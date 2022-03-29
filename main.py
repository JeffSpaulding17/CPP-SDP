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
# csv file name and path
pi_id = os.popen("cat pi.id")
file_name = "pi-" + pi_id + "-temp-data.csv"
file_path = os.path.abspath( os.path.join(os.path.dirname(__file__), file_name) )

# csv row data
col_headers = ["Timestamp (s)", "Temperature (F)", "Humidity (%% air-water mix compared to dew point)"]
col_data = list()

# csv last line sent to master pi and the number of lines in the csv file
csv_file_len = 0
last_master_csv_line = 0



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
    col_data.append(data_list)


##################################################
#                                                #
#                   COMPILE CSV                  #
#                                                #
##################################################
# Create the csv file with permissions of -rw-rw-rw
def make_csv(add_header=False):
    global csv_file_len
    os.umask(0)
    with open(file_path, "w+") as csv_file:
        if(add_header):
            csv_wr_obj = csv.writer(csv_file)
            csv_wr_obj.writerow(col_headers)
            csv_file_len += 1
    return

###############################

# Write data to the csv file and remove old data after
def write_to_csv(header=False):
    global csv_file_len
    global last_master_csv_line
    with open(file_path, "a", newline="") as csv_file:
        csv_wr_obj = csv.writer(csv_file)
        if(header):
            csv_wr_obj.writerow(col_headers)
            csv_file_len += 1
        else:
            last_master_csv_line += len(col_data)
            csv_wr_obj.writerows(col_data)
            csv_file_len += len(col_data)
            col_data.clear()
    return

###############################

# Send the csv file to the master RPi
def send_csv_to_master():
    global last_master_csv_line
    global csv_file_len
    
    # If no data was gathered since last asking, do nothing
    if(last_master_csv_line == csv_file_len):
        return
    
    # Send master the lines it has not yet received before
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
    
    
    # TODO: asynchronous TCP server
    
    
    # Check if previous run had .csv file, if so delete it
    if os.path.exists(file_path):
        delete_csv_data()
    
    # Create the csv file
    make_csv(add_header=True)
    
    # Gather 5 data points before writing to csv file
    send_to_master_flag = False
    while not send_to_master_flag:
        for i in range(5):
            get_row_data(temp_sense_obj, start_time)
            time.sleep(2)
        write_to_csv()
    
    # Clear the csv file content and test if it was deleted
    #delete_csv_data()
    with open(file_path, "r") as csv_file:
        csv_read_obj = csv.reader(csv_file)
        rows = []
        for row in csv_read_obj:
            rows.append(row)
        print(rows)
    
    
#########################################################       


if __name__ == "__main__":
    main()