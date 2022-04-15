##################################################################
###                                                            ###
###             TEMPERATURE SENSORS GATHERING DATA             ###
###                                                            ###
###             BY: DEREK MATA & JEFFERY SPAULDING             ###
###                PROFESSOR OMAR SDP & ECE 5590               ###
###                        SPRING 2022                         ###
###                                                            ###
##################################################################

# Library for csv functions
import csv

# General OS interaction libraries
import os
import time

# Libraries for sensor data retrieval 
import board
import busio
import adafruit_dht
import adafruit_ina260

# Custom made libraries
import sensor


##################################################
#                                                #
#                PROGRAM CONSTANTS               #
#                                                #
##################################################
# csv file name and path
pi_id = os.popen("cat pi.id")
file_name = "pi-" + str(pi_id) + "-temp-data.csv"
file_path = os.path.abspath( os.path.join(os.path.dirname(__file__), file_name) )

# csv row data
col_headers = ["Timestamp (s)", "Temperature (F)", "Humidity (%% air-water mix compared to dew point)"]
col_data = list()



##################################################
#                                                #
#                  DATA GATHERING                #
#                                                #
##################################################
# Get the temperature data from the sensor on RPi
def get_sensor_data(temp_sense_obj: sensor.temperature_sensor):
    temp_f = temp_sense_obj.get_temp()
    humidity = temp_sense_obj.get_humidity()
    return (temp_f, humidity)

###############################

# Get the timestamp, temperature, and humidity for that row
def get_row_data(temp_sense_obj: sensor.temperature_sensor, start_time: float):
    temp_f, humidity = get_sensor_data(temp_sense_obj)
    timestamp = timestamp = time.time() - start_time
    data_list = [str(round(timestamp, 5)), str(round(temp_f, 2)), str(round(humidity, 2))]
    print("\t", end="")
    print(data_list)
    col_data.append(data_list)
    return


##################################################
#                                                #
#                   COMPILE CSV                  #
#                                                #
##################################################
# Create the csv file with permissions of -rw-rw-rw
def make_csv(add_header=False):
    os.umask(0)
    with open(file_path, "w+") as csv_file:
        if(add_header):
            csv_wr_obj = csv.writer(csv_file)
            csv_wr_obj.writerow(col_headers)
        csv_file.close()
    return

###############################

# Write data to the csv file and remove old data after
def write_to_csv(header=False):
    global col_data
    with open(file_path, "a", newline="") as csv_file:
        csv_wr_obj = csv.writer(csv_file)
        if(header):
            csv_wr_obj.writerow(col_headers)
        else:
            csv_wr_obj.writerows(col_data)
            col_data.clear()
    return
    


##################################################
#                                                #
#                  MAIN FUNCTION                 #
#                                                #
##################################################
def main():  
    # Start system timer for timestamps
    start_time = time.time()
      
    # Create Temperature Sensor object
    temp_sense_obj = sensor.temperature_sensor()    
    
    # Create power sensor object
    # power_sense_obj = sensor.power_sensor()
    
    # Check if previous run had .csv file, if not make it
    if not os.path.exists(file_path):
        make_csv(add_header=True)
    
    # Gather data points every second until user presses CTRL+C or end with exception, then write everything to csv file
    try:
        print("Now gathering data from temperature sensor [timestamp, temp_f, humidity %]:")
        while True:
            get_row_data(temp_sense_obj, start_time)
            time.sleep(1)
    except KeyboardInterrupt as k:
        print("Stopping data collection...")
    except Exception as e:
        print(f"Error during data collection!!!  -->  {e}")
    finally:
        print("Now writing data to .csv file:")
        write_to_csv()
    
    # END
    print("\n\n********************************************************************")
    print("*                                                                  *")
    print("*                        Program complete!!                        *")
    print("*                                                                  *")
    print("********************************************************************")
    
    
#########################################################       


if __name__ == "__main__":
    main()