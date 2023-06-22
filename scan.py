import socket
import os
import signal
import time
import threading
import sys
import subprocess
from queue import Queue
from datetime import datetime


# Main Function
def main():
    socket.setdefaulttimeout(0.30)
    print_lock = threading.Lock()
    discovered_ports = []

    # Welcome Banner
    print("-" * 60)
    print("\033[1;34m    ____             __  _____")
    print("   / __ \____  _____/ /_/ ___/_________ _____  ____  ___  _____")
    print("  / /_/ / __ \/ ___/ __/\__ \/ ___/ __ `/ __ \/ __ \/ _ \/ ___/")
    print(" / ____/ /_/ / /  / /_ ___/ / /__/ /_/ / / / / / / /  __/ /")
    print("/_/    \____/_/   \__//____/\___/\__,_/_/ /_/_/ /_/\___/_/\033[0m")
    print("-" * 60)
    time.sleep(1)
    target = input("Enter your target IP address or URL here: ")
    error = ("Invalid Input")
    try:
        t_ip = socket.gethostbyname(target)
    except (UnboundLocalError, socket.gaierror):
        print("\n\033[1;31m[-]Invalid format. Please use a correct IP or web address[-]\033[0m\n")
        sys.exit()
    
    # Banner
    print("-" * 60)
    print("\033[1;36mScanning target " + t_ip)
    print("Time started: " + str(datetime.now()))
    print("-" * 60)
    t1 = datetime.now()

    def portscan(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            portx = s.connect((t_ip, port))
            with print_lock:
                print("\033[1;32mPort {} is open\033[0m".format(port))
                discovered_ports.append(str(port))
            portx.close()
        except (ConnectionRefusedError, AttributeError, OSError):
            pass

    def threader():
        while True:
            worker = q.get()
            portscan(worker)
            q.task_done()
      
    q = Queue()
     
    for x in range(200):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()

    for worker in range(1, 65536):
        q.put(worker)

    q.join()

    t2 = datetime.now()
    total = t2 - t1
    print("\033[1;36mPort scan completed in {}\033[0m".format(str(total)))
    print("-" * 60)
    print("\033[1;33mScanner recommends the following Nmap scan:")
    print("*" * 60)
    print("nmap -p{ports} -sV -sC -T4 -Pn -oA {ip} {ip}".format(ports=",".join(discovered_ports), ip=target))
    print("*" * 60)
    nmap = "nmap -p{ports} -sV -sC -T4 -Pn -oA {ip} {ip}".format(ports=",".join(discovered_ports), ip=target)
    t3 = datetime.now()
    total1 = t3 - t1

    def automate():
        choice = '0'
        while choice == '0':
            print("Would you like to run Nmap or quit to terminal?")
            print("-" * 60)
            print("1 = Run suggested Nmap scan")
            print("2 = Run another port scan")
            print("3 = Exit to terminal")
            print("-" * 60)
            choice = input("Option Selection: ")
            if choice == "1":
                try:
                    print(nmap)
                    os.mkdir(target)
                    os.chdir(target)
                    os.system(nmap)
                    convert = "xsltproc "+target+".xml -o "+target+".html"
                    os.system(convert)
                    t3 = datetime.now()
                    total1 = t3 - t1
                    print("-" * 60)
                    print("\033[1;36mCombined scan completed in {}\033[0m".format(str(total1)))
                    print("Press enter to quit...")
                    input()
                except FileExistsError as e:
                    print(e)
                    exit()
            elif choice == "2":
                main()
            elif choice == "3":
                sys.exit()
            else:
                print("Please make a valid selection")
                automate()
    
    automate()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        quit()
