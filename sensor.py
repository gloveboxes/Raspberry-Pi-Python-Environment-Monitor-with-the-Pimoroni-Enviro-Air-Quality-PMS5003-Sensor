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

        self.pid = os.getpid()
        self.py = psutil.Process(self.pid)

        # pause for a moment to allow the pms5003 to settle
        time.sleep(1.0)

    async def readSensor(self):
        try:
            samples = 15
            avg = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            telemetry = None

            for i in range(samples):
                readings = self.pms5003.read()
                for j in range(14):
                    avg[j] += readings.data[j]
                await asyncio.sleep(1)

            telemetry = {
                # PM1.0 ug/m3 (ultrafine particles)
                "PM1-0": int(avg[0]/samples),
                # PM2.5 ug/m3 (combustion particles, organic compounds, metals)
                "PM2-5": int(avg[1]/samples),
                # PM10 ug/m3  (dust, pollen, mould spores)
                "PM10": int(avg[2]/samples),
                "Temperature": round(self.bme280.get_temperature(), 1),
                "Pressure": round(self.bme280.get_pressure(), 1),
                "Humidity": round(self.bme280.get_humidity(), 1),
                "Mem": self.py.memory_info()[0]
            }

        except ReadTimeoutError:
            self.pms5003 = PMS5003()
            print('Timeout reading PMS5003 Sensor')
            telemetry = None

        return telemetry
