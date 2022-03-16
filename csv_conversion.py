##################################################################
###                                                            ###
###                     CSV FILE CREATION                      ###
###                                                            ###
###                       BY: DEREK MATA                       ###
###                 ECE 5590 - COMPUTER NETWORK                ###
###                        SPRING 2022                         ###
###                                                            ###
##################################################################

# How to write to csv files: https://www.geeksforgeeks.org/writing-csv-files-in-python/


# Library for csv functions
import csv

# General file interaction library
import os

# File path for .csv 
file_name = "test.csv"
file_path = os.path.abspath( os.path.join(os.path.dirname(__file__), file_name) )

# Column headers for data
col_headers = ["Timestamp (s)", "Temperature (F)", "Humidity (%% air-water mix compared to dew point)"]

# Testing data to store to each row
row_test_values = [
    ["0.12", "94.5", "12.1"],
    ["0.24", "93.2", "11.5"],
    ["0.36", "93.6", "11.8"],
    ["0.48", "93.8", "11.7"]
]



#########################
#                       #
#      MAIN FUNCTION    #
#                       #
#########################
def main():   
    # Create the csv file and then open it
    with open(file_path, "w+", newline="") as csv_file:
        # Create the csv object to write to file
        csv_writer_obj = csv.writer(csv_file)
        
        # First write the headers
        csv_writer_obj.writerow(col_headers)
        
        # Write all of the test values 
        csv_writer_obj.writerows(row_test_values)

    # Open the file using excel
    os.startfile(file_path)
    
    
    
    
    
if __name__ == "__main__":
    main()
