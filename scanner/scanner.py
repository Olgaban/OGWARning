import sys
import asyncio
from bleak import BleakScanner
import subprocess

sys.path.append(".")

timeout_seconds = 5
address_to_look_for = 'masked'
service_id_to_look_for = 'masked'

OUR_UUID = "0000feaa-0000-1000-8000-00805f9b34fb"

runDetect = True
advertisingMessage = ""


def detection_callback(device, advertisement_data):
    global advertisingMessage

    for some_id in advertisement_data.service_data:
        message = advertisement_data.service_data.get(some_id)
        if some_id != OUR_UUID:
            continue

        message = str(message)[14:-1]
        print(message, device.address)

        if advertisingMessage == message:
            continue

        advertisingMessage = message

        # ADVERTISE THE MESSAGE
        subprocess.call(f"sudo python3 ../advertise/advertise_ble.py -d '{message}'", shell=True)


async def run():
    scanner = BleakScanner()
    scanner.register_detection_callback(detection_callback)
    await scanner.start()
    await asyncio.sleep(timeout_seconds)
    await scanner.stop()


def stop():
    runDetect = False


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    while runDetect:
        loop.run_until_complete(run())
