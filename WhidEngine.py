import requests
import re
from pathlib import Path
from urllib.parse import urlencode, quote_plus

class WhidEngine(object):

    # NOTE: check if the panel is reachable
    def __init__(self, panel):
        try:
            if not "ESPloit" in requests.get(panel, timeout=1).text:
                print("\033[91mError 404, are you connected on the right AP?")
                self.update_firmware()

        except Exception as e:
            print (e)
            print("\033[91mError, couldn't reach the Wifi Portal !\033[0m")


    # NOTE: this update use the last firmware on Github
    # You may need to build a new one with your keyboard mapping
    def update_firmware(self):
         update = "https://github.com/exploitagency/ESPloitV2/releases"
         update = requests.get(update).text
         regex = re.compile("exploit.*\.bin")
         last = "https://github.com/" + regex.findall(update)[0]

         name = "firmware/"+"-".join(last.split('/')[-2:])
         download = Path(name)
         if not download.exists():
             print("Downloading the last release: %s" % last)
             r = requests.get(last, stream=True)
             if r.status_code == 200:
                 with open(name, 'wb') as f:
                     for chunk in r:
                         f.write(chunk)

    # NOTE: send the payload to the /runlivepayload page
    def send_payload(self, user_converted, panel):
        payloads = { "livepayload":user_converted, "livepayloadpresent":1}
        encoded  = urlencode( payloads, quote_via=quote_plus)
        try:
            print('Sending payload to %s' % panel)
            if not "200" in str(requests.post(panel, data=encoded)):
                print("\033[91mError 404, are you connected on the right AP?")

        except Exception as e:
            print("\033[91mError, couldn't reach the Wifi Portal !")


    # NOTE : mapping is use for retro-compatibility
    def convert_to_keymap(self, user_input, payload, mapping=False):
        if mapping:
            # Dirty version, if you don't want to upgrade the firmware
            fr_mapping = './mazqwAZQW&é"\'(-è_çà)^$Mù,?;:!§1234567890'
            en_mapping = '<>;qwazQWAZ1234567890-[]:\'mM,./?!@#$%^&*()'
            user_converted = user_input.translate(str.maketrans(fr_mapping,en_mapping))
        else:
            user_converted = user_input

        # Merge the payload and the user input
        user_converted = payload % user_converted
        return user_converted
