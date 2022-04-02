import asyncio
import struct
from bleak import BleakScanner

timeout_seconds = 30
address_to_look_for = 'masked'
service_id_to_look_for = 'masked'


def detection_callback(device, advertisement_data):
    for some_id in advertisement_data.service_data:
        print(device.address, "RSSI:", device.rssi, advertisement_data)
        print(advertisement_data.service_data)
        byte_data = advertisement_data.service_data.get(some_id)
        num_to_test = struct.unpack_from('<I', byte_data, 0)
        print(num_to_test)


async def run():
    scanner = BleakScanner()
    scanner.register_detection_callback(detection_callback)
    await scanner.start()
    await asyncio.sleep(timeout_seconds)
    await scanner.stop()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
