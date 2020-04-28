import time
from pms5003 import PMS5003, ReadTimeoutError
import json
import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
import sys
import psutil

async def main():

    avg = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    samples = 15

    conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
    print(conn_str)
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
    await device_client.connect()

    pms5003 = PMS5003()
    time.sleep(1.0)

    pid = os.getpid()
    py = psutil.Process(pid)

    async def message_listener(device_client):
        while True:
            message = await device_client.receive_message()  # blocking call
            print("the data in the message received was ")
            print(message.data)
            print("custom properties are")
            print(message.custom_properties)

    asyncio.create_task(message_listener(device_client))

    try:
        while True:
            try:
                avg = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                for i in range(samples):
                    readings = pms5003.read()
                    for j in range(14):
                        avg[j] += readings.data[j]
                    time.sleep(1)

                telemetry = {
                    # PM1.0 ug/m3 (ultrafine particles)
                    "PM1-0": int(avg[0]/samples),
                    # PM2.5 ug/m3 (combustion particles, organic compounds, metals)
                    "PM2-5": int(avg[1]/samples),
                    # PM10 ug/m3  (dust, pollen, mould spores)
                    "PM10": int(avg[2]/samples),
                    "Mem": py.memory_info()[0]
                }

                print(telemetry)

                data = json.dumps(telemetry)

                await device_client.send_message(data)

                time.sleep(60*10)

            except ReadTimeoutError:
                pms5003 = PMS5003()
                print('Timeout reading PMS5003 Sensor')
            except:
                print("Unexpected error:", sys.exc_info()[0])

    except KeyboardInterrupt:
        pass

    await device_client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())

    # If using Python 3.6 or below, use the following code instead of asyncio.run(main()):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
