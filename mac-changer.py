import subprocess
import optparse

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

try:
    sys_output = subprocess.check_output(["cat", "/sys/class/net/" + options.interface + "/address"])
except:
    print("[!] Interface doesn't exist.")
    exit()

try:
    sys_output = subprocess.check_output(["cat", "/sys/class/net/" + options.interface + "/address"])
    print("[*] Current MAC: " + sys_output.strip())
except:
    print("[!] No such interface.")

change_mac(options.interface, options.new_mac)
current_mac = subprocess.check_output(["cat", "/sys/class/net/" + options.interface + "/address"])

if current_mac.strip() == options.new_mac:
    print("[+] MAC address changed to " + options.new_mac)
else:
    print("[!] Unable to change MAC address.")
