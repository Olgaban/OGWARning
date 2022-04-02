# How to run this command
# sudo python3 ./advertise_ble.py -d example_msg

import os
import sys
import subprocess
import argparse

if (sys.version_info > (3, 0)):
    DEVNULL = subprocess.DEVNULL
else:
    DEVNULL = open(os.devnull, 'wb')
# The default data
data = "default_message"

parser = argparse.ArgumentParser(prog='advertise_ble', description=__doc__)
parser.add_argument("-d", "--data", nargs='?', const=data, type=str, default=data, help='Data to advertise.')

parser.add_argument('-s', '--stop', action='store_true', help='Stop advertising ble.')

parser.add_argument("-v", "--verbose", action='store_true', help='Print lots of debug output.')

options = parser.parse_args()

data = options.data


def verboseOutput(text=""):
    if options.verbose:
        sys.stderr.write(text + "\n")


def encode_data(data):
    i = 0
    cur_data = []
    try:
        scheme = ""
        if data.startswith(scheme):
            cur_data.append(0)
            i += len(scheme)
    except Exception as e:
        raise Exception("Invalid cur_data scheme")

    while i < len(data):
        if data[i] == '.':
            extension = ""
            if data.startswith(extension, i):
                cur_data.append(0)
                i += len(extension)
            else:
                cur_data.append(0x2E)
                i += 1
        else:
            cur_data.append(ord(data[i]))
            i += 1
    return cur_data


def encode_message(data):
    encoded_data = encode_data(data)
    encoded_data_length = len(encoded_data)

    verboseOutput("Encoded data length: " + str(encoded_data_length))

    if encoded_data_length > 18:
        raise Exception("Encoded data too long (max 18 bytes)")

    message = [
        0x02,  # Flags length
        0x01,  # Flags data type value
        0x1a,  # Flags data

        0x03,  # Service UUID length
        0x03,  # Service UUID data type value
        0xaa,  # 16-bit Eddystone UUID
        0xfe,  # 16-bit Eddystone UUID

        5 + len(encoded_data),  # Service Data length
        0x16,  # Service Data data type value
        0xaa,  # 16-bit Eddystone UUID
        0xfe,  # 16-bit Eddystone UUID

        0x10,  # Eddystone-data frame type
        0xed,  # txpower
    ]

    message += encoded_data

    return message


def advertise(data):
    print("Advertising: " + data)
    verboseOutput("Advertising: " + data)
    message = encode_message(data)

    # Prepend the length of the whole message
    message.insert(0, len(message))

    # Pad message to 32 bytes for hcitool
    while len(message) < 32: message.append(0x00)

    # Make a list of hex strings from the list of numbers
    message = map(lambda x: "%02x" % x, message)

    # Concatenate all the hex strings, separated by spaces
    message = " ".join(message)
    verboseOutput("Message: " + message)

    subprocess.call("sudo hciconfig hci0 up", shell=True, stdout=DEVNULL)

    # Stop advertising
    subprocess.call("sudo hcitool -i hci0 cmd 0x08 0x000a 00", shell=True, stdout=DEVNULL)

    # Set message
    subprocess.call("sudo hcitool -i hci0 cmd 0x08 0x0008 " + message, shell=True, stdout=DEVNULL)

    # Resume advertising
    subprocess.call("sudo hcitool -i hci0 cmd 0x08 0x000a 01", shell=True, stdout=DEVNULL)


def stopAdvertising():
    print("Stopping advertising")
    verboseOutput("Stopping advertising")
    subprocess.call("sudo hcitool -i hci0 cmd 0x08 0x000a 00", shell=True, stdout=DEVNULL)


if __name__ == "__main__":
    try:
        if options.stop:
            stopAdvertising()
        else:
            advertise(data)
    except Exception as e:
        sys.stderr.write("Exception: " + str(e) + "\n")
        exit(1)
