#!/usr/bin/env python

import subprocess
import re
import argparse


def take_arg():
    collect = argparse.ArgumentParser()
    collect.add_argument("-i", "--interface", dest="interface", help="The interface to change it's MAC address")
    collect.add_argument("-m", "--mac", dest="address", help="The MAC address to be used")
    option = collect.parse_args()
    if not option.interface:
        collect.error("[-] Kindly specify the interface or use --help for more information")
    elif not option.address:
        collect.error("[-] Kindly specify the MAC address to be used or use --help for more information")
    else:
        return option


def get_current_mac(interface):
    get_mac = subprocess.check_output(["ifconfig", interface])
    get_mac2 = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", get_mac.decode("utf-8"))
    # .decode("utf-8) will change the result from bytes to string for python3 to work it
    former_mac = get_mac2.group(0)
    if not former_mac:
        print("[-] Could not find MAC address")
    else:
        print("your current MAC address is " + str(former_mac))
    return former_mac


def change_mac(interface, address, form):
    print("[+] Bringing down " + interface)
    subprocess.call(["ifconfig", interface, "down"])
    print("[+] Changing " + form + " to " + address)
    subprocess.call(["ifconfig", interface, "hw", "ether", address])
    print("[+] Bringing up " + interface)
    subprocess.call(["ifconfig", interface, "up"])


def get_new_mac(interface, address, form):
    new_mac = subprocess.check_output(["ifconfig", interface])
    new_mac2 = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", new_mac.decode("utf-8"))
    changed_mac = new_mac2.group(0)
    if changed_mac == address:
        print("[+] MAC address has successfully been changed from " + form + " to " + address)
    else:
        print("[-] Failed to change MAC address from " + form + " to " + address)
        print("[-] The code needs a super-user permission, kindly run in root")
        print("[-] Try using another address")


print("This code should be run in python2, python3 has difficulties in processing the code.")
options = take_arg()
forms = get_current_mac(options.interface)
change_mac(options.interface, options.address, forms)
get_new_mac(options.interface, options.address, forms)
