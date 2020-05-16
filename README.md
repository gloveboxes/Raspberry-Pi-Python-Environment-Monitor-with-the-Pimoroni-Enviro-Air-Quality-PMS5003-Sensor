# Tutorial: Azure IoT Central and Particulate Matter Monitoring  

## Background

Born of necessity, this project tracks the air quality over Sydney during the height of the Australian bush fires. I wanted to gauge when it was safe to go outside, or when it was better to close up the apartment and stay in for the day.

| Sydney, Dec 2019 | Particulate matter readings|
| ---- | ---|
| ![](resources/sydney-height-of-bush-fires.jpg) | Readings for PM 2.5 and PM 10 approx 1000. Healthy levels should be between 0 ~ 10. ![](resources/pm-readings-dec-10-2019.png) |

This is Sydney on a clear day, the photo was taken in May 2020, alas, during the COVID-19 pandemic lock down. On the upside, there is close to zero air pollution.

![](resources/sydney-height-of-pandemic.jpg)


---

## Introduction

In this hands-on lab, you will learn how to create and debug a Python application on a Raspberry Pi with [Visual Studio Code](https://code.visualstudio.com/?WT.mc_id=pycon-blog-dglover) and the [Remote SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh&WT.mc_id=pycon-blog-dglover) extension. The app requires the [Pimoroni Enviro+ pHAT](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-enviro-plus), and reads data from the PMS5003 particulate matter (PM) and BME280 sensors and streams the data to [Azure IoT Central](https://azure.microsoft.com/services/iot-central/).

---

## Terminology

1. Computer refers to your desktop or laptop computer running Linux, macOS, or Windows 10.
2. Raspberry Pi refers to your Raspberry Pi:)

---

## Parts required

1. Raspberry Pi, SD Card, and Raspberry Pi power supply
2. [Pimoroni Enviro+ pHAT](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-enviro-plus)
3. PMS5003 Particulate Matter Sensor with Cable available from [Pimoroni](https://shop.pimoroni.com/products/pms5003-particulate-matter-sensor-with-cable) and eBay.

This lab depends on Visual Studio Code and Remote SSH development. Remote SSH development is supported on Raspberry Pis built on ARMv7 chips or better. The Raspberry Pi Zero is built on ARMv6 architecture. It can run the solution, but it does not support Remote SSH development.

![](resources/azure-iot-central-air-quality-monitor.png)

---

## Acknowledgements

This tutorial build on the [Azure IoT Python SDK 2](https://github.com/Azure/azure-iot-sdk-python/tree/master/azure-iot-device/samples) samples.

## Lab set up

### Setting up a Raspberry Pi headless

Follow these steps:

1. Using the [Raspberry Pi Imager](https://www.raspberrypi.org/blog/raspberry-pi-imager-imaging-utility/) create a bootable SD Card Operating System image. From the Raspberry Pi Imager menu select Raspbian (other), then Raspbian List. Raspberry Pi Lite is headless, there is no UI, only a command line interface accessible over the network via SSH.
2. The Raspberry Pi Imager will eject the SD Card when the OS image has been copied to the SD Card. You need to physically eject the SD Card from your computer and reinsert.
3. Configure the [Raspberry Pi WiFi](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md) networking]
4. Enable SSH on the SD Card. Create an empty file named **ssh** on the SD Card drive named **boot**.
5. Remove the Raspberry Pi Bootable image from your computer and insert into your Raspberry Pi
6. Attach the [Pimoroni Enviro+ pHAT](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-enviro-plus) and  PMS5003 Particulate Matter sensor.
7. Power on your Raspberry Pi
8. Wait for a minute for the Raspberry Pi to boot the first time
9. The find and make a note of the Raspberry Pi IP Address. The easiest way is from your computer, start a command prompt or terminal window. Try the following commands.

    ```bash
    ping raspberrypi.local
    ```

    If that doesn't work, try

    ```bash
    ping raspberrypi
    ```

    For other options see these [notes](https://www.raspberrypi.org/documentation/remote-access/ip-address.md).
10. Now log into your Raspberry Pi with SSH.
    1. From your computer, start a command prompt or terminal window.
    2. Run the following command

        ```bash
        ssh pi@Your Raspberry Pi IP Address
        ```

        for example

        ```bash
        ssh pi@192.168.1.25
        ```

    3. You will be prompted to trust the Raspberry Pi
    4. You will be prompted for the default Raspberry Pi password. The default password is **raspberry**.
11. Update your Raspberry Pi.
    1. From the SSH session you just started, run the following command on the Raspberry Pi. This will update the Raspberry Pi Operating System, install two required Linux packages, and reboot the Raspberry Pi

        ```bash
        sudo apt update && sudo apt install -y git python3-pip && sudo apt upgrade -y && sudo reboot
        ```

12. Wait for the Raspberry Pi to reboot. You can tell when the Raspberry Pi is ready when the green LED on the Raspberry Pi stops flickering.

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

### Clone the Azure IoT Central Python Environment Monitoring Solution

Clone the Environment Monitoring solution to your Raspberry Pi. From the SSH session, run the following command.

```bash
git clone https://github.com/gloveboxes/Raspberry-Pi-Python-Environment-Monitor-with-the-Pimoroni-Enviro-Air-Quality-PMS5003-Sensor.git environment
```

![](resources/raspberry-pi-set-up-completed.png)

---

## Computer set up

1. Install the [git client](https://git-scm.com/downloads).
2. Clone the Environment Monitoring solution to your computer. From your computer, start a command prompt or terminal window. Change to your preferred projects directory on your computer. Make a note of the directory as you will need to refer to that directory shortly. Run:

    ```bash
    git clone https://github.com/gloveboxes/Raspberry-Pi-Python-Environment-Monitor-with-the-Pimoroni-Enviro-Air-Quality-PMS5003-Sensor.git environment
    ```


## Set up SSH Authentication between your computer and Raspberry Pi

![ssh login](resources/ssh-login.jpg)

Setting up a public/private key pair for [SSH](https://en.wikipedia.org/wiki/Secure_Shell) authentication is a secure and fast way to authenticate from your computer to the Raspberry Pi. This is recommended for this hands-on lab.

### Set up SSH for Windows Users

The SSH utility guides you through the process of setting up a secure SSH channel for Visual Studio Code and the Raspberry Pi.

You will be prompted for:

- The Raspberry Pi Network IP Address,
- The Raspberry Pi login name and password. The Raspberry Pi **default** login name is **pi**, and the default password is **raspberry**.

1. From Windows File Explorer, open the directory you cloned the Environment Monitor solution into.
2. Open the **environment** directory
3. Open the **scripts** folder
4. Double click the **windows-setup-ssh.cmd**

### Set up SSH for Linux and macOS Users

The SSH utility guides you through the process of setting up a secure SSH channel for Visual Studio Code and the Raspberry Pi.

You will be prompted for:

- The Raspberry Pi Network IP Address,
- The Raspberry Pi login name and password

1. Open a Terminal window
2. Copy and paste the following command, and press **ENTER**

    ```bash
    curl https://raw.githubusercontent.com/gloveboxes/Raspberry-Pi-Python-Environment-Monitor-with-the-Pimoroni-Enviro-Air-Quality-PMS5003-Sensor/master/scripts/ssh-setup.sh | bash
    ```

---

## Set up Visual Studio Code on your computer

This hands-on lab requires Visual Studio Code. Visual Studio Code is a code editor and is one of the most popular **Open Source** projects on [GitHub](https://github.com/microsoft/vscode). It runs on Linux, macOS, and Windows.

1. Install Visual Studio Code from [here](https://code.visualstudio.com/). 

---

## Start a Remote SSH Connection

1. Start Visual Studio Code
2. Press **F1** to open the Command Palette, type **ssh connect** and select **Remote-SSH: Connect to Host**

3. Select the **pylab-pi** configuration
    <br/>

    ![open the ssh project](resources/vs-code-open-ssh-connection.png)

    <br/>
4. Check the Remote SSH has connected.

    It will take a moment to connect, then the SSH Status in the bottom lefthand corner of Visual Studio Code will change to **>< SSH:pylab-pi**.
    <br/>

    ![](resources/vs-code-remote-ssh-connected.png)




2. Click on the links to install the following Visual Studio Code extensions
    1. [Python extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
    2. [Docker for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)

    Ensure when you are installing the Python and Docker extensions you are installing into SSH. The following is an example of adding the Python extension into the SSH session.

    ![](resources/vs-code-install-python.png)

![](resources/computer-set-up-completed.png)

---

## Configure Azure IoT Central

## Creating an Azure IoT Central Application

### What is Azure IoT Central

Easily connect, monitor and manage your Internet of Things (IoT) assets at scale. [Azure IoT Central](https://azure.microsoft.com/en-in/services/iot-central/?WT.mc_id=pycon-blog-dglover) is a hosted, extensible software as a service (SaaS) platform that simplifies setup of your IoT solution and helps reduce the burden and costs of IoT management, operations and development. Provide customers superior products and service while expanding your business possibilities.

![Azure IoT Central](resources/azure-iot-central.jpg)

We are going to create an Azure IoT Central application, then a device, and finally a device **connection string** needed for the application that will run in the Docker container.

![](resources/azure_iot_central.png)

## Create a New IoT Central Application

1. Open the [Azure IoT Central](https://azure.microsoft.com/en-au/services/iot-central/?WT.mc_id=pycon-blog-dglover) in a new browser tab, then click **Getting started**.

2. Next, you will need to sign with your **Microsoft** Personal, or Work, or School account. If you do not have a Microsoft account, then you can create one for free using the **Create one!** link.

    ![iot central](resources/iot-central-login.png)

3. Create a new Azure IoT Central application, select **New Application**. This takes you to the **Create Application** page.

4. Select **Build as app**

    ![](resources/iot-central-build-first-app.png)

5. Select **Custom app**

    ![](resources/iot-central-custom-app.png)

### Create a **New application**

Specify **Application name**, **URL**, enable **7 day free trial**, and complete the registration form. Then click **Create**.

![](resources/iot-central-new-application.png)

1. Add new Device Template

    Click **Device templates**

    ![](resources/iot-central-device-template.png)

2. Select **IoT device** template type

    ![](resources/iot-central-new-iot-device-template.png)

3. Create an **IoT Device** Template

    1. Select **IoT device**, 
    2. Click **Next:Customise**, 
    3. Click **Next: Review**, 
    4. Click **Create**.
    5. Name your template **Air Quality Monitor**, and press **Enter**

#### Import a Capability Model

1. Add an Interface

    1. Click **Import capability model**
    2. Navigate to the folder you cloned the solution into.
    3. Select **Air Quality Monitor.json** and open

2. Create a view
    1. Click **Views**
        ![](resources/iot-central-create-a-view.png)
    2. Select **Visualizing the device**
    3. Select the Particular Matter telemetry
        ![](resources/iot-central-add-tile-particular-matter.png)
    4. Click **Add Tile**
    5. Select Humidity, Pressure, and Temperature telemetry.
        ![](resources/iot-central-add-tile-bme280.png)
    6. Click **Add Tile**
    7. Drag the Humidity, Pressure, Temperature tile so that it lines up with the Particular Matter tile.
        ![](resources/iot-central-tiles-align.png)
    8. Save the view
        ![](resources/iot-central-view-save.png)
        <br/>

3. Click **Publish** to publish the template
    <br/>
    ![](resources/iot-central-template-publish.png)

---

## Create a device



![](resources/azure-iot-central-set-up-completed.png)

## Configure Python App for IoT Central



```text
SCOPE_ID={IoT Central ID Scope}
DEVICE_ID={your device id}
DEVICE_KEY={your device key}
````

## References

[Tutorial: Create and connect a client application to your Azure IoT Central application (Python)](https://docs.microsoft.com/en-us/azure/iot-central/core/tutorial-connect-device-python)