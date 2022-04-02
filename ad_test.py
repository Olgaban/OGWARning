import asyncio
import struct

from bleak import BleakScanner

timeout_seconds = 10
address_to_look_for = 'masked'
service_id_to_look_for = 'masked'


def detection_callback(device, advertisement_data):
    for some_id in advertisement_data.service_data:
        message = advertisement_data.service_data.get(some_id)
        # print(some_id)
        # num_to_test = struct.unpack_from('<I', message, 0)
        if some_id != "0000feaa-0000-1000-8000-00805f9b34fb":
            continue
        print(message)
        # print(device.address, "RSSI:", device.rssi, advertisement_data)
        # print(device.address, advertisement_data.service_data)


async def run():
    scanner = BleakScanner()
    scanner.register_detection_callback(detection_callback)
    await scanner.start()
    await asyncio.sleep(timeout_seconds)
    await scanner.stop()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())