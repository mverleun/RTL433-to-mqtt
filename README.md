# RTL433 to mqtt gateway

This small script is a cheap and easy way to start with IoT projects.
By using the great rtl_433 software and a cheap RTL-SDR receiver it will listen to all kinds of devices transmitting at the 433,92 Mhz frequency.

Quite likely it will receive information from weatherstations in your area,
if you don't own one, your neighbours might!
It will also receive signals from remote controls that are popular to use to
control the lights.

It's one way. You can receive a lot of information, but you can not send any!

## MQTT Topics
The gateway will receive information from the SDR receiver and publish them in JSON format to the topic `sensors/rtl_433`. (Without the slash!)

Subtopics are created from this JSON line allowing to easily subscribe to specific sensors.

Testing can be done with the following command:
```bash
mosquitto_sub -h mqtt.example.com -p 1883 -v -t "sensors/#"
```

This will generate output like this:

```
sensors/rtl_433 {"time" : "2018-07-05 09:48:17", "model" : "AlectoV1 Wind Sensor", "id" : 36, "channel" : 1, "battery" : "OK", "wind_speed" : 0.000, "wind_gust" : 0.200, "wind_direction" : 315, "mic" : "CHECKSUM"}

sensors/rtl_433/AlectoV1 Wind Sensor/time 2018-07-05 09:48:17
sensors/rtl_433/AlectoV1 Wind Sensor/id 36
sensors/rtl_433/AlectoV1 Wind Sensor/channel 1
sensors/rtl_433/AlectoV1 Wind Sensor/battery OK
sensors/rtl_433/AlectoV1 Wind Sensor/wind_speed 0.0
sensors/rtl_433/AlectoV1 Wind Sensor/wind_gust 0.2
sensors/rtl_433/AlectoV1 Wind Sensor/wind_direction 315
sensors/rtl_433/AlectoV1 Wind Sensor/mic CHECKSUM
sensors/rtl_433 {"time" : "2018-07-05 09:48:22", "model" : "AlectoV1 Rain Sensor", "id" : 140, "channel" : 0, "battery" : "OK", "rain_total" : 621.750, "mic" : "CHECKSUM"}

sensors/rtl_433/AlectoV1 Rain Sensor/time 2018-07-05 09:48:22
sensors/rtl_433/AlectoV1 Rain Sensor/id 140
sensors/rtl_433/AlectoV1 Rain Sensor/channel 0
sensors/rtl_433/AlectoV1 Rain Sensor/battery OK
sensors/rtl_433/AlectoV1 Rain Sensor/rain_total 621.75
sensors/rtl_433/AlectoV1 Rain Sensor/mic CHECKSUM
sensors/rtl_433 {"time" : "2018-07-05 09:48:48", "model" : "AlectoV1 Wind Sensor", "id" : 36, "channel" : 1, "battery" : "OK", "wind_speed" : 0.000, "wind_gust" : 0.000, "wind_direction" : 270, "mic" : "CHECKSUM"}

sensors/rtl_433/AlectoV1 Wind Sensor/time 2018-07-05 09:48:48
sensors/rtl_433/AlectoV1 Wind Sensor/id 36
sensors/rtl_433/AlectoV1 Wind Sensor/channel 1
sensors/rtl_433/AlectoV1 Wind Sensor/battery OK
sensors/rtl_433/AlectoV1 Wind Sensor/wind_speed 0.0
sensors/rtl_433/AlectoV1 Wind Sensor/wind_gust 0.0
sensors/rtl_433/AlectoV1 Wind Sensor/wind_direction 270
sensors/rtl_433/AlectoV1 Wind Sensor/mic CHECKSUM
sensors/rtl_433 {"time" : "2018-07-05 09:48:59", "model" : "AlectoV1 Rain Sensor", "id" : 140, "channel" : 0, "battery" : "OK", "rain_total" : 621.750, "mic" : "CHECKSUM"}

sensors/rtl_433/AlectoV1 Rain Sensor/time 2018-07-05 09:48:59
sensors/rtl_433/AlectoV1 Rain Sensor/id 140
sensors/rtl_433/AlectoV1 Rain Sensor/channel 0
sensors/rtl_433/AlectoV1 Rain Sensor/battery OK
sensors/rtl_433/AlectoV1 Rain Sensor/rain_total 621.75
sensors/rtl_433/AlectoV1 Rain Sensor/mic CHECKSUM
```

Note that spaces can be used in topic names!

This could be used to subscribe to selected topics, e.g. if you want to know the battery status of all the sensors you could subscribe to the topic `sensors/rtl_433/+/battery`.

This would look similar to this:

```bash
mosquitto_sub -h mqtt.example.com -p 1883 -v -t "sensors/rtl_433/+/battery"
sensors/rtl_433/AlectoV1 Rain Sensor/battery OK
sensors/rtl_433/AlectoV1 Wind Sensor/battery OK
sensors/rtl_433/AlectoV1 Rain Sensor/battery OK
```


## Installation
Before you get started you'll have to install some packages.

First install software using the command:

``` bash
apt-get update && apt-get install -y rtl-sdr librtlsdr-dev librtlsdr0 git automake libtool cmake
```

This will install all the software you need to build the latest version of the rtl_433 receiver
software.

Next download and build the receiver software:

```bash
git clone https://github.com/merbanan/rtl_433.git && cd rtl_433/ && mkdir build && cd build && cmake ../ && make && make install
```
The last step is to install the python MQTT library:

```bash
pip3 install paho-mqtt
```

## Configuration
Copy the file `config.py.example` to `config.py` and change the settings by editting this file.

Once you're done you can connect the RTL-SDR to a USB port and start using the
python script.

## Docker
A `Dockerfile` is included as well. Use it if you want to run this software in a Docker container.

Navigate to the `src` directory of this project and enter the following command:

```bash
docker build -t rtl433-mqtt-gateway .
```

This will build the image needed to start a container. When the build process is completed start the container:

```bash
docker run --name rtl_433 -d --rm --privileged -v /dev/bus/usb:/dev/bus/usb  rtl433-mqtt-gateway
```
