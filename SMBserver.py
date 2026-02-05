#!/usr/share/env python3

import signal
import sys
import argparse
from termcolor import colored
from impacket import smbserver
from impacket.examples import logger

def def_handler(sig, frame):

	print(colored("\n[!] Saliendo...\n",'red'))
	sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def args():
	parser=argparse.ArgumentParser(description="Custom SMB Server")
	parser.add_argument("-n", "--new", dest="new", type=str, required=True, help="Name of the new folder you are going to create and share")
	parser.add_argument("-r", "--route", dest="route", type=str, required=True, help="The route where the SMB service will be set up")
	parser.add_argument("-p", "--port", dest="port", type=int, help="The port where the service will be set up", default=445)

	options = parser.parse_args()
	return options

class MySMBServer(smbserver.SimpleSMBServer): #subclass

    def __init__(self, *args, **kwargs): #constructor
        super().__init__(*args, **kwargs)
        self.vistas = set() #connId already seen

    def addShare(self, name, path, comment='', readOnly='yes'):
        super().addShare(name, path, comment, readOnly) #call original method

        real = self._SimpleSMBServer__server #give me the actual SMB engine that's underneath
        original = real.getConnectionData

        def hook(connId, checkStatus=True):
            data = original(connId, checkStatus)

            if connId not in self.vistas: #anti-spam
                ip = data.get("ClientIP", "UNKNOWN")
                print(colored(f"\n[+] Cliente SMB activo desde {ip}\n",'green'))
                self.vistas.add(connId) #save as seen

            return data

        real.getConnectionData = hook #when SMB server calls "getConnectionData" use hook function

def start_server(new, route, port):

	server = MySMBServer(

		listenAddress="0.0.0.0", #ip
		listenPort=port #port
	)


	server.addShare(f"{new}",f"{route}",readOnly="no")

	server.setSMB2Support(True)
	server.setSMBChallenge('')

	print(colored("\n[+] Se ha iniciado el servidor SMB\n",'yellow'))
	server.start()


if __name__ == '__main__':

	try:
		opt = args()
		start_server(opt.new,opt.route,opt.port)
	except PermissionError:
		print(colored("\n\n[!] Error, tienes que ejecutar este script con permisos root\n\n",'red'))
		sys.exit(1)
