#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    WiCC (Wifi Cracking Camp)
    Second version of the original WiCC tool at https://github.com/pabloibiza/WiCC
    GUI tool for wireless pentesting on WEP and WPA/WPA2 networks.
    Project developed by Pablo Sanz Alguacil, Miguel Yanes Fernández.
"""


class Client:
    client_id = ""
    station_MAC = ""
    first_seen = ""
    last_seen = ""
    power = 0
    packets = 0
    bssid = ""
    probed_bssids = ""

    def __init__(self, id, station_MAC, first_seen, last_seen, power, packets, bssid, probed_bssids):
        self.client_id = id
        self.station_MAC = station_MAC
        self.first_seen = first_seen
        self.last_seen = last_seen
        self.power = power
        self.packets = packets
        self.bssid = bssid
        self.probed_bssids = probed_bssids

    def get_bssid(self):
        """
        Getter for the bssid parameter
        :return: bssid of the client

        :Author: Miguel Yanes Fernández
        """
        return self.bssid

    def get_mac(self):
        """
        Getter fro the MAC parameter
        :return: station mac of the client

        :Author: Miguel Yanes Fernández
        """
        return self.station_MAC

    def get_list(self):
        """
        Create and return a list of parameters
        :return: list of all class parameters

        :Author: Miguel Yanes Fernández
        """
        return [
            self.client_id,
            self.station_MAC,
            self.first_seen,
            self.first_seen,
            self.last_seen,
            self.power,
            self.power,
            self.packets,
            self.bssid,
            self.probed_bssids,
        ]
