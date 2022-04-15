##################################################################
###                                                            ###
###                  TEMPERATURE SENSOR CLASS                  ###
###                                                            ###
###             BY: DEREK MATA & JEFFERY SPAULDING             ###
###                PROFESSOR OMAR SDP & ECE 5590               ###
###                        SPRING 2022                         ###
###                                                            ###
##################################################################

# Libraries for sensor data retrieval 
import time
import board
import busio
import adafruit_dht
import adafruit_ina260
 
# Initial the dht device, with data pin connected to:
# dhtDevice = adafruit_dht.DHT11(board.D4)
 
# you can pass DHT11 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
 

# DHT11 temperature sensor from Adafruit
class temperature_sensor:
    # Constructor --> initialize the temperature sensor object with adafruit library, and create temperatrues and humidity
    def __init__(self):
        self.dhtDevice = adafruit_dht.DHT11(board.SCL, use_pulseio=False)
        self.temp_c = 0
        self.temp_f = 0
        self.humidity = 0.0        
    
    # Get temperature from sensor in both C and F
    def get_temp(self):
        try:
            self.temp_c = self.dhtDevice.temperature
            self.temp_f = self.temp_c * (9/5) + 32
        except RuntimeError as err:
            print(err.args[0])
        except Exception as err:
            self.dhtDevice.exit()
            raise err
        
        return self.temp_f
    
    # Get the humidity from sensor in terms of percentage of air-water mixture relative to dew point
    def get_humidity(self):
        try:
            self.humidity = self.dhtDevice.humidity
        except RuntimeError as err:
            print(err.args[0])
        except Exception as err:
            self.dhtDevice.exit()
            raise err
        
        return self.humidity
    

# INA260 power sensor from Adafruit  
class power_sensor:
    # Constructor --> initialize the power sensor object with adafruit library and i2c bus
    #                 set the voltage, current, and power initially to zero
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.inaDevice = adafruit_ina260.INA260(self.i2c)
        self.inaDevice.mode = adafruit_ina260.Mode.CONTINUOUS
        self.current = 0
        self.voltage = 0
        self.power = 0
        
    # Get the current, voltage, power data
    def get_cvp(self):
        try:
            self.current = self.inaDevice.current
            self.voltage = self.inaDevice.voltage
            self.power = self.inaDevice.power
        except RuntimeError as err:
            print(err.args[0])
        except Exception as err:
            raise err
        
        return (self.current, self.voltage, self.power)
