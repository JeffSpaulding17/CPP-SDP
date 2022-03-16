# Temperature/Humidity Sensor Network using an SDN and How to Reduce its Power Consumption

### Code developed by Jeffery Spaulding and Derek Mata

---

### Summary
In this project, we will be developing a network of temperature sensors controlled by an SDN controller.  We will collect temperature and humidity data from an array of Raspberry Pis, compile the data into `.csv` files, pass those files over the SDN network to a master Raspbery Pi, and record the power consumption of this process.  We will record the overall power reduction by increasing the number of connections to each slave Raspberry Pi, therefore reducing the number of hops to the master Raspberry Pi.


### Overall Progress / What Needs to be Done
- [x] Developed temperature/humidity senesor gathering code
- [ ] Developed `.csv` compilation of sensor data
- [ ] Properly configure the SDN to be able to send packets over the network
- [ ] Send data over the SDN to the master Raspberry Pi
- [ ] Gather power consumption data for this process
- [ ] Reduce the overall power consumption 
- [ ] Gather reduced power consumption for this process
- [ ] Visualize the data


### Dependencies used
- `time`
- `board`
- `adafruit_dht`
- `os`
- `csv`


### Files in Repository
- `sensor.py`
- `csv_conversion.py`
