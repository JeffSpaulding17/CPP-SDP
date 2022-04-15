#!/bin/bash

# After reboot --> test i2c and spi functionality
ls /dev/i2c* /dev/spi*
echo "init_rpi_script_1.sh success if above you see --> /dev/i2c-1 /dev/spidev0.0 /dev/spidev0.1"
echo "If correct, press ENTER key, otherwise press CTRL+C..."
read correct
echo "Now checking GPIO functionality..."
python3 blinkatest.py
echo "If above says:"
echo "Hello blinka!"
echo "Digital IO ok!"
echo "I2C ok!"
echo "SPI ok!"
echo "done"
echo "THEN, press ENTER key, otherwise press CTRL+C..."
read correct2


# Now will install all dependencies
echo "Now installing all dependencies..."
sudo pip install python-csv
sudo pip3 install adafruit-circuitpython-dht
sudo apt-get install libgpiod2
sudo pip3 install adafruit-circuitpython-ina260