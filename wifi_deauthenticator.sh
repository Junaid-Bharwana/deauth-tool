#!/bin/bash

start_airmon_ng() {
  airmon-ng start wlan0
}

stop_airmon_ng() {
  airmon-ng stop wlan0
}

deauthentication_menu() {
  clear
  echo "Deauthentication Menu"
  echo "---------------------"
  echo "1. Check WiFi List"
  echo "2. Set Channel"
  echo "3. Deauthenticate WiFi"
  echo "4. Show Connected Devices"
  echo "5. Deauthenticate Specific Device(s)"
  echo "6. Deauthenticate Multiple WiFi"
  read -p "Enter your choice: " choice
  case $choice in
    1) check_wifi_list ;;
    2) set_channel ;;
    3) deauthenticate_wifi ;;
    4) show_connected_devices ;;
    5) deauthenticate_specific_device ;;
    6) deauthenticate_multiple_wifi ;;
    *) echo "Invalid choice" ;;
  esac
}

while true; do
  clear
  echo "WiFi Deauthenticator"
  echo "-------------------"
  echo "1. Start"
  echo "2. Stop"
  echo "3. Deauthentication Menu"
  read -p "Enter your choice: " choice
  case $choice in
    1) start_airmon_ng ;;
    2) stop_airmon_ng ;;
    3) deauthentication_menu ;;
    *) echo "Invalid choice" ;;
  esac
done
