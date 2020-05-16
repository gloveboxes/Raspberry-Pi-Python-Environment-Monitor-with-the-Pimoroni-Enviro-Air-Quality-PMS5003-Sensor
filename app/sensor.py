from pms5003 import PMS5003, ReadTimeoutError
from bme280 import BME280
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
import psutil
import os
import asyncio
import time


class Sensor():

    def __init__(self):
        self.pms5003 = PMS5003()
        self.bus = SMBus(1)
        self.bme280 = BME280(i2c_dev=self.bus)
        self.bme280.get_pressure()  # prime bme sensor as first reading not accurate
        self.msgId = 0
        self.nextRead = None
        self.avg = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.pid = os.getpid()
        self.py = psutil.Process(self.pid)

        # pause for a moment to allow the pms5003 to settle
        time.sleep(1.0)

    async def readSensor(self):
        try:
            samples = 15
            telemetry = None

            if self.nextRead is None or self.nextRead < time.time():
                self.avg = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                # don't read pms5003 sensor for another 10 minutes = 10 minutes time 60 seconds
                self.nextRead = time.time() + (10 * 60)

                for i in range(samples):
                    readings = self.pms5003.read()
                    for j in range(14):
                        self.avg[j] += readings.data[j]
                    await asyncio.sleep(1)

            self.msgId += 1

            telemetry = {
                # PM1.0 ug/m3 (ultrafine particles)
                "pm1": int(self.avg[0]/samples),
                # PM2.5 ug/m3 (combustion particles, organic compounds, metals)
                "pm25": int(self.avg[1]/samples),
                # PM10 ug/m3  (dust, pollen, mould spores)
                "pm10": int(self.avg[2]/samples),
                "temperature": round(self.bme280.get_temperature(), 1),
                "pressure": round(self.bme280.get_pressure(), 1),
                "humidity": round(self.bme280.get_humidity(), 1),
                "mem": self.py.memory_info()[0],
                "msgId": self.msgId
            }

        except ReadTimeoutError:
            self.pms5003 = PMS5003()
            print('Timeout reading PMS5003 Sensor')
            telemetry = None

        return telemetry
