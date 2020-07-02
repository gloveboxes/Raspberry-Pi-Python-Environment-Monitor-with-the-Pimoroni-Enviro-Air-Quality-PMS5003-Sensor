# Module 2: Install Azure IoT Edge on your Raspberry Pi

---

## Index

* Module 1: [Create an Azure IoT Central application](../module_1_create_iot_hub/README.md)
* Module 2: [Set up your Raspberry Pi](../module_2_set_up_raspberry_pi/README.md)
* Module 3: [Set up your development environment](../module_3_set_up_computer/README.md)
* Module 4: [Run the solution](../module_4_building_the_solution/README.md)

* [Home](../../README.md)

---

## Hardware requirements

1. Raspberry Pi 2 or better, SD Card, and Raspberry Pi power supply
2. [Pimoroni Enviro+ pHAT](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-enviro-plus)
3. PMS5003 Particulate Matter Sensor with Cable available from [Pimoroni](https://shop.pimoroni.com/products/pms5003-particulate-matter-sensor-with-cable) and eBay.

## Raspberry Pi 4 Tips and Tricks

This lab does not need a Raspberry Pi 4, but if you are using one then here are some tips and tricks I like to use for my Raspberry Pi.

### Booting from high speed USB3 storage

As we will be building Docker images on the Raspberry Pi 4 so I would recommend a fast SD Card or a high speed USB3 Flash or SSD drive.

* I use a Samsung [USB 3.1 Flash Drive FIT Plus 128GB](https://www.samsung.com/us/computing/memory-storage/usb-flash-drives/usb-3-1-flash-drive-fit-plus-128gb-muf-128ab-am/) or USB3 SSD drive. See the [5 of the Fastest and Best USB 3.0 Flash Drives](https://www.makeuseof.com/tag/5-of-the-fastest-usb-3-0-flash-drives-you-should-buy/)
* For instruction on booting from USB3 see [How to Boot Raspberry Pi 4 From a USB SSD or Flash Drive](https://www.tomshardware.com/how-to/boot-raspberry-pi-4-usb). Note, at the time of writing, set the *FIRMWARE_RELEASE_STATUS* to *stable* rather than *beta*.


### Optionally overclocking a Raspberry Pi 4

Though not a requirement, the machine learning inference times will be improved by overclocking the Raspberry Pi 4. You will need a Raspberry Pi heat sink if you overclock. See the [How to overclock Raspberry Pi 4](https://magpi.raspberrypi.org/articles/how-to-overclock-raspberry-pi-4) article for more information. 

I use the following settings in the ```/boot/config.txt```.

```text
over_voltage=6
arm_freq=2000
gpu_freq=700
```

---

## Raspberry Pi set up

### Create the Raspberry Pi OS Image

I recommend using Raspberry Pi OS Lite as it takes less resources than the full Raspberry Pi Desktop version. If you've not set up a Raspberry Pi before then this is a great guide. "[Setting up a Headless Pi](https://learn.pimoroni.com/tutorial/sandyj/setting-up-a-headless-pi)". Be sure to use the WiFi network as your development computer.



### Start Raspberry Pi and update

1. Attach the [Pimoroni Enviro+ pHAT](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-enviro-plus) and  PMS5003 Particulate Matter sensor.
2. Insert SD Card or USB3 drive, and power on your Raspberry Pi.
3. Log into the Raspberry Pi over your network

    ```bash
    ssh pi@raspberrypi.local
    ```

    or depending on your network settings try

    ```bash
    ssh pi@raspberrypi
    ```

4. Update and reboot

    ```bash
    sudo apt update && sudo apt install -y git python3-pip && sudo apt full-upgrade && sudo reboot
    ```

---

## Install Docker on the Raspberry Pi

1. Log into your Raspberry Pi

    ```bash
    ssh pi@raspberrypi.local
    ```

2. From the SSH session run the following command.

    ```bash
    curl -sSL get.docker.com | sh && sudo usermod pi -aG docker && sudo reboot
    ```

---

### Install the following Python Packages

From the SSH session you started in the previous step install the following required Python packages. Run the following command.

```bash
pip3 install ptvsd azure-iot-device psutil enviroplus RPi.GPIO pylint autopep8
```

### Install the Pimoroni Enviro+ Python library

From the SSH session, run the following commands.

```bash
git clone https://github.com/pimoroni/enviroplus-python
cd enviroplus-python
sudo ./install.sh
```

You will also be prompted to install the samples. Select **y** as they will be useful for you to understand how to extend the solution.

---

## Clone the Raspberry Pi Air Quality Monitor Solution

1. Log into your Raspberry Pi

    ```bash
    ssh pi@raspberrypi.local
    ```

2. From the SSH session, clone the solution repository to the Raspberry Pi

    ```bash
    git clone https://github.com/gloveboxes/Raspberry-Pi-Python-Environment-Monitor-with-the-Pimoroni-Enviro-Air-Quality-PMS5003-Sensor.git raspberry-pi-air-quality-monitor
    ```

---

**[NEXT](../module_3_set_up_computer/README.md)**

---
