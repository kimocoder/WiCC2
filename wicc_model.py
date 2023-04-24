#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    WiCC (Wifi Cracking Camp)
    Second version of the original WiCC tool at https://github.com/pabloibiza/WiCC
    GUI tool for wireless pentesting on WEP and WPA/WPA2 networks.
    Project developed by Pablo Sanz Alguacil, Miguel Yanes Fernández.
"""

from wicc_interface import Interface
from wicc_network import Network
from wicc_client import Client


class Model:
    interfaces = []
    networks = []
    clients = []
    network_filters = [False, False]
    net_attack_instances = []  # object instances of the net attack classes

    def __init__(self):
        """
        Class constructor. Initializes the list of interfaces and networks
        """
        self.interfaces = []
        self.networks = []

    def set_interfaces(self, interfaces):
        """
        Sets the list of interfaces as the one received as parameter
        :param interfaces: list of objects of the class Interface
        :return:
        """
        self.interfaces = interfaces

    def add_interface(self, name, address, type, power, channel):
        """
        Add a single interface given the parameters to create a new one
        :param name: string for the name of the interface
        :param address: string for the physical address of the interface
        :param type: string for the type of mode of the interface (managed, monitor, ...)
        :param power: int for the dBm of power of the interface
        :param channel: int for the selected channel
        :return:
        """
        interface = Interface(name, address, type, power, channel)
        if not self.interfaces.__contains__(interface):
            self.interfaces.append(interface)

    def set_networks(self, networks):
        """
        Creates the new networks based on the list of parameters recevied
        :param networks: list of lists of network parameters
        :return:
        """
        list_networks = []

        first_time_empty = False
        id = 1

        handshake = False
        password = ""
        clients = 0

        for network in networks:
            # id = ""
            bssid = ""
            first_seen = ""
            last_seen = ""
            channel = 0
            speed = 0
            privacy = ""
            cipher = ""
            authentication = ""
            power = 0
            beacons = 0
            ivs = 0
            lan_ip = ""
            essid = ""
            for cont, pair in enumerate(network):
                if cont == 0:
                    bssid = pair
                elif cont == 1:
                    first_seen = pair
                elif cont == 10:
                    ivs = pair
                elif cont == 11:
                    lan_ip = pair
                elif cont == 13:
                    # parameter 12 shows the length of the essid, so it's not necessary
                    essid = pair
                elif cont == 2:
                    last_seen = pair
                elif cont == 3:
                    channel = pair
                elif cont == 4:
                    speed = pair
                elif cont == 5:
                    privacy = pair
                elif cont == 6:
                    cipher = pair
                elif cont == 7:
                    authentication = pair
                elif cont == 8:
                    power = pair
                elif cont == 9:
                    beacons = pair
            if bssid == '':
                if first_time_empty:
                    break
                first_time_empty = True
            elif bssid != 'BSSID':
                list_networks.append(Network(id, bssid, first_seen, last_seen, channel, speed, privacy, cipher,
                                             authentication, power, beacons, ivs, lan_ip, essid, handshake,
                                             password, clients))
                id += 1
        self.networks = list_networks

    def set_clients(self, clients):
        """
        Given a list of parameters of clients, filters them and creates and store those clients
        :param clients: lists of lists of parameters of clients
        :return:
        """
        list_clients = []
        id = 1
        for client in clients:
            station_MAC = ""
            first_seen = ""
            last_seen = ""
            power = 0
            packets = 0
            bssid = ""
            probed_bssids = ""

            for cont, pair in enumerate(client):
                if cont == 0:
                    station_MAC = pair
                elif cont == 1:
                    first_seen = pair
                elif cont == 2:
                    last_seen = pair
                elif cont == 3:
                    power = pair
                elif cont == 4:
                    packets = pair
                elif cont == 5:
                    bssid = pair
                elif cont == 6:
                    probed_bssids = pair
            if bssid != ' (not associated) ':
                client = Client(id, station_MAC, first_seen, last_seen, power, packets, bssid, probed_bssids)
                list_clients.append(client)
                self.add_client_network(bssid, client)
                id += 1

        self.clients = list_clients

    def add_client_network(self, bssid, client):
        """
        Add a client to the specified network. Searchs for the network and calls the method to add one client.
        :param bssid: bssid of the network
        :return:
        """
        for network in self.networks:
            if network.get_bssid() == bssid[1:]:
                network.add_client(client)
                return

    def compare_interfaces(self, interfaces):
        """
        Compares a given list of interfaces with the local ones. Checks the names.
        :param interfaces: List of parameters of interfaces
        :return: boolean depending on whether both lists are equivalent
        """
        for interface in interfaces:
            for local_interface in self.interfaces:
                if str(interface[0]) == str(local_interface.get_name()):
                    return True
        return False

    def get_parameters(self):
        """
        Creates a list of parameters for both interfaces and networks.
        Will be used by the view to print these parameters
        :return: list of parameters of all interfaces, list of parameters of all networks

        :author: Miguel Yanes Fernández & Pablo Sanz Alguacil
        """
        list_interfaces = [object.get_list() for object in self.interfaces]
        list_networks = []

        if self.network_filters[1]:
            list_networks.extend(
                network.get_list()
                for network in self.networks
                if network.get_clients() != 0
            )
        else:
            list_networks.extend(object.get_list() for object in self.networks)
        return list_interfaces, list_networks

    def search_network(self, network_id):
        """
        Search a network given an id
        :param network_id: id of the network
        :return: network object, if found

        :Author: Miguel Yanes Fernández
        """
        return next(
            (
                network
                for network in self.networks
                if network.get_id() == network_id
            ),
            None,
        )

    def get_interfaces(self):
        """
        Get the interfaces array
        :return: interfaces

        :Author: Miguel Yanes Fernández
        """
        return self.interfaces

    def get_mac(self, interface_name):
        """
        Returns an inteface's mac
        :param interface_name:
        :return: mac address

        :author: Miguel Yanes Fernández
        """
        for interface in self.interfaces:
            if interface.get_name() == interface_name:
                return interface.get_address()

    def set_filters(self, wps_filter_status, clients_filter_status):
        """
        Sets the filters for the networks.
        :param wps_filter_status:
        :param clients_filter_status:
        :return:

        :author: Pablo Sanz Alguacil
        """
        self.network_filters[0] = wps_filter_status
        self.network_filters[1] = clients_filter_status

    def clear_interfaces(self):
        """
        Resets the interfaces variable
        :return: none

        :Author: Miguel Yanes Fernández
        """
        self.interfaces = []

    def clear_networks(self):
        """
        Resets the networks variable
        :return: none

        :Author: Miguel Yanes Fernández
        """
        self.networks = []

    def add_net_attack(self, mac, object_reference):
        """
        Add a net_attack object, inlcudin the network mac (bssid)
        :param mac: network mac
        :param object_reference: net_attack object reference
        :return: none

        :Author: Miguel Yanes Fernández
        """
        self.net_attack_instances.append([mac, object_reference])

    def get_net_attack(self, mac):
        """
        Search a net attack object with a given mac address
        :param mac: mac address of the network
        :return: net attack object, if found

        :author: Miguel Yanes Fernández
        """
        return next(
            (
                self.net_attack_instances[i][1]
                for i in range(len(self.net_attack_instances))
                if self.net_attack_instances[i][0] == mac
            ),
            None,
        )

