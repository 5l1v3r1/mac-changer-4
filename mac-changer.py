import subprocess
import optparse
import re

def get_arguments():

    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address.")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address.")

    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("Interface not specified.")
    elif not options.new_mac:
        parser.error("MAC address not specified.")

    return options

def change_mac(interface, new_mac):

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

options = get_arguments()

def get_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result.decode('utf-8'))

    try:
        return mac_result.group(0)
    except:
        print("[-] Unable to read MAC address.")

if get_mac(options.interface):
    current_mac = get_mac(options.interface)
else:
    exit()
print("[*] Current MAC: "+ current_mac)

change_mac(options.interface, options.new_mac)

current_mac = get_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address changed to " + options.new_mac)
else:
    try:
        print("[-] Unable to change MAC address to " + options.new_mac)
    except:
        print("[-] Unable to change MAC address.")
        exit()
