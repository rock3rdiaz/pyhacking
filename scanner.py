#!/usr/bin/python3

import nmap

scanner = nmap.PortScanner()

print("Welcome, this is a simple nmap automation tool")
print("<------------------------------------------------------->")
ip_address = input("Please enter the IP address you want to scan: ")
print("The IP you entered is: {0:s}".format(ip_address))
type(ip_address)

response = input("""\nPlease enter the type of scab you want to run
                    1)SYN ACK Scan 
                    2)UDP Scan
                    3)Comprehensive Scan\n""")
print("You have selected option {0:s}".format(response))

if response == '1':
    print("Nmap Version {0:s}".format(str(scanner.nmap_version())))
    scanner.scan(ip_address, '1-1024', '-v -sS')
    print(scanner.scaninfo())
    print("IP status: {0:s}".format(str(scanner[ip_address].state())))
    print(scanner[ip_address].all_protocols())
    print("The open port: {0:s}".format(str(scanner['tcp'].keys())))

elif response == '2':
    print("Nmap Version {0:s}".format(str(scanner.nmap_version())))
    scanner.scan(ip_address, '1-1024', '-v -sU')
    print(scanner.scaninfo())
    print("IP status: {0:s}".format(str(scanner[ip_address].state())))
    print(scanner[ip_address].all_protocols())
    print("The open port: {0:s}".format(str(scanner['udp'].keys()))) 

elif response == '3':
    print("Nmap Version {0:s}".format(str(scanner.nmap_version())))
    scanner.scan(ip_address, '1-1024', '-v -sS -sV -sC -A -O')
    print(scanner.scaninfo())
    print("IP status: {0:s}".format(str(scanner[ip_address].state())))
    print(scanner[ip_address].all_protocols())
    print("The open port: {0:s}".format(str(scanner['tcp'].keys()))) 

elif int(response) >= 4:
    print("Please a enter a valid option")


