import sys
import asyncio
from bleak import BleakScanner
import subprocess
from commands import commands


sys.path.append(".")

timeout_seconds = 5
address_to_look_for = 'masked'
service_id_to_look_for = 'masked'

OUR_UUID = "0000feaa-0000-1000-8000-00805f9b34fb"

runDetect = True

actual_n = -1


def detection_callback(device, advertisement_data):
    global advertisingMessage, actual_n

    for some_id in advertisement_data.service_data:
        message = advertisement_data.service_data.get(some_id)
        if some_id != OUR_UUID:
            continue

        message = str(message)[14:-1]
        number = int(message[:3])
        message_key = int(message[3:])
        print(commands[message_key], device.address)

        if number > actual_n or number == 999:
            actual_n = number
            subprocess.call(f"sudo python3 ./advertise_ble.py -d '{message}'", shell=True)
            with open("plik.txt", "w") as file:
                file.write('0' * (3 - len(str(number)))+ str(number) + commands[message_key])


async def run():
    scanner = BleakScanner()
    scanner.register_detection_callback(detection_callback)
    await scanner.start()
    await asyncio.sleep(timeout_seconds)
    await scanner.stop()


def main():
    i = 0
    loop = asyncio.get_event_loop()
    while runDetect:
        loop.run_until_complete(run())

if __name__ == '__main__':
    main()
