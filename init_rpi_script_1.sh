#!/bin/bash

# Script to install dependencies onto RPi
echo "Updating apt-get..."
cd ~
sudo apt-get install update
sudo apt-get install upgrade
sudo apt-get clean

echo "Installing pip and pip3..."
sudo apt install python3-pip
sudo apt install python-pip
sudo pip install wheel
sudo pip3 install --upgrade setuptools

echo "Getting circuitpython from adafruit..."
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py

echo "rebooting... run init_rpi_script_1.sh after reboot!"
sudo reboot