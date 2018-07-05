#
# Docker file to create an image that contains enough software to listen to events on the 433,92 Mhz band,
# filter these and publish them to a MQTT broker.
#
# The script resides in a volume and should be modified to meet your needs.
#
# The example script filters information from weather stations and publishes the information to topics that
# Domoticz listens on.
#
# Special attention is required to allow the container to access the USB device that is plugged into the host.
# The container needs priviliged access to /dev/bus/usb on the host.
#
# docker run --name rtl_433 -d -e MQTT_HOST=<mqtt-broker.example.com>   --privileged -v /dev/bus/usb:/dev/bus/usb  <image>

FROM python:3.6.3
MAINTAINER Marco Verleun

LABEL Description="This image is used to start a script that will monitor for events on 433,92 Mhz" Vendor="MarCoach" Version="1.0"

# Install additional modules
RUN pip install paho-mqtt

#
# First install software packages needed to compile rtl_433 and to publish MQTT events
#
RUN apt-get update && apt-get install -y \
	rtl-sdr \
	librtlsdr-dev \
	librtlsdr0 \
	git \
	automake \
	libtool \
	cmake

#
# Pull RTL_433 source code from GIT, compile it and install it
#
RUN git clone https://github.com/merbanan/rtl_433.git \
	&& cd rtl_433/ \
	&& mkdir build \
	&& cd build \
	&& cmake ../ \
	&& make \
	&& make install

#
# Copy config, script and make it executable
#
COPY rtl2mqtt.py /scripts/rtl2mqtt.py
COPY config.py /scripts/config.py
RUN chmod +x /scripts/rtl2mqtt.py

#
# When running a container this script will be executed
#

ENTRYPOINT ["/scripts/rtl2mqtt.py"]
