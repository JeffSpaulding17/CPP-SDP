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
import sys
import time

# Libraries for sensor data retrieval 
import board
import adafruit_dht

# Custom made libraries
import sensor


##################################################
#                                                #
#                PROGRAM CONSTANTS               #
#                                                #
##################################################
# csv file information
file_name = "test.csv"
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
    temp_c, temp_f = temp_sense_obj.get_temp()
    humidity = temp_sense_obj.get_humidity()
    return (temp_f, temp_c, humidity)



##################################################
#                                                #
#                   COMPILE CSV                  #
#                                                #
##################################################
# Create the csv file with permissions of -rw-rw-rw
def make_csv(add_header=False):
    try:
        os.umask(0)
        os.open(file_path, os.O_CREAT | os.O_RDWR, 0o666)
        os.close(file_path)
        if(add_header):
            write_to_csv(header=True)
    except FileExistsError as exist:
        print("File already exists, passing")
        pass
    except Exception as err:
        print("Error making csv file: " + err)
        sys.exit(1)
    return

###############################

# Write data to the csv file and remove old data after
def write_to_csv(header=False):
    with open(file_path, "a", newline="") as csv_file:
        csv_wr_obj = csv.writer(csv_file)
        if(header):
            csv_wr_obj.writerow(col_headers)
        else:
            csv_wr_obj.writerows(col_data)
    col_data.clear()
    return

###############################

# Send the csv file to the master RPi
def send_csv_to_master():
    pass

###############################

# Delete the content from the old csv file by 
# deleting and remaking file
def delete_csv_data(add_header=False):
    try:
        os.remove(file_path)
        make_csv(add_header=add_header)
    except FileNotFoundError as fnf_err:
        print("no csv file to remove: " + fnf_err)
    except Exception as err:
        print("cannot remove csv file: " + err)
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
    
    # Create the csv file, and its writer object
    make_csv(add_header=True)
    
    # Get 5 rows of data from temperature sensor --> 10 seconds
    for i in range(5):
        temp_f, temp_c, humidity = get_sensor_data(temp_sense_obj)
        timestamp = time.time() - start_time
        data_list = [str(round(timestamp, 5)), str(round(temp_f, 2)), str(round(humidity, 2))]
        col_data.append(data_list)
        time.sleep(2)
    
    # Write col_data to csv file
    write_to_csv()
    
    # Clear the csv file content and test if it was deleted
    delete_csv_data()
    with open(file_path, "r") as csv_file:
        csv_read_obj = csv.reader(csv_file)
        rows = []
        for row in csv_read_obj:
            rows.append(row)
        print(rows)
    
    
#########################################################       


if __name__ == "__main__":
    main()