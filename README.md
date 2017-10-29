# RTL433 to mqtt

This small script is a cheap and easy way to start with IoT projects.
By using the great rtl_433 software and a cheap RTL-SDR receiver it will
listen to all kinds of devices transmitting at the 433,92 Mhz frequency.

Quite likely it will receive information from weatherstations in your area,
if you don't own one, your neighbours might!
It will also receive signals from remote controls that are popular to use to
control the lights.

It's one way. You can receive a lot of information, but you can not send any!

Before you get started you'll have to install some packages.

First install software using the command:

apt-get update && apt-get install -y \
        rtl-sdr \
        librtlsdr-dev \
        librtlsdr0 \
        git \
        automake \
        libtool \
        cmake

This will install all the software you need to build the latest version of the rtl_433 receiver
software.

Next download and build the receiver software:

git clone https://github.com/merbanan/rtl_433.git \
        && cd rtl_433/ \
        && mkdir build \
        && cd build \
        && cmake ../ \
        && make \
        && make install

The last step is to install the python MQTT library:

pip3 install paho-mqtt

Once you're done you can connect the RTL-SDR to a USB port and start using the
python script.

Don't forget to change the settings in the python script. They should match your mqttserver.
