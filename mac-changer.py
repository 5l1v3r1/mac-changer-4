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
    with open('/sys/class/net/' + options.interface + '/address') as f:
        sys_output = f.readlines()
        for i in sys_output:
            sys_output = i
        print("[*] Current MAC: " + sys_output.strip())
except:
    print("[!] No such interface.")
    exit()

change_mac(options.interface, options.new_mac)

with open('/sys/class/net/' + options.interface + '/address') as f:
    sys_output = f.readlines()
    for i in sys_output:
        sys_output = i

if sys_output.strip() == options.new_mac:
    print("[+] MAC address changed to " + options.new_mac)
else:
    print("[!] Unable to change MAC address.")
