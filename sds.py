#!/usr/bin/python

import serial
import time
import struct

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600) #Set port, e.g. for Linux '/dev/ttyUSB0', Windows: 'COM3' etc.

ser.flushInput()


def sensor_set_wake():
    bytes = [b'\xaa',  # Head
             b'\xb4',  # Command ID
             b'\x06',  # Data byte 01
             b'\x01',  # Data byte 02, 01: set mode
             b'\x01',  # Data byte 03, 01: work
             b'\x00',  # Data byte 04
             b'\x00',  # Data byte 05
             b'\x00',  # Data byte 06
             b'\x00',  # Data byte 07
             b'\x00',  # Data byte 08
             b'\x00',  # Data byte 09
             b'\x00',  # Data byte 10
             b'\x00',  # Data byte 11
             b'\x00',  # Data byte 12
             b'\x00',  # Data byte 13
             b'\xff',  # Data byte 14, FF: response from all sensors, set to ID for unique sensor
             b'\xff',  # Data byte 15, FF: response from all sensors, set to ID for unique sensor
             b'\x06',  # Checksum
             b'\xab']  # Tail
    for  b in bytes:
        ser.write(b)


def sensor_set_sleep():
    bytes = [b'\xaa',  # Head
             b'\xb4',  # Command ID
             b'\x06',  # Data byte 01
             b'\x01',  # Data byte 02, 01: set mode
             b'\x00',  # Data byte 03, 00: sleep
             b'\x00',  # Data byte 04
             b'\x00',  # Data byte 05
             b'\x00',  # Data byte 06
             b'\x00',  # Data byte 07
             b'\x00',  # Data byte 08
             b'\x00',  # Data byte 09
             b'\x00',  # Data byte 10
             b'\x00',  # Data byte 11
             b'\x00',  # Data byte 12
             b'\x00',  # Data byte 13
             b'\xff',  # Data byte 14, FF: query all devices
             b'\xff',  # Data byte 15, FF: query all devices
             b'\x05',  # Checksum
             b'\xab']  # Tail
    for b in bytes:
        ser.write(b)


def sensor_query_data():

    bytes = 0

    while bytes != b'\xaa':
        bytes = ser.read(size=1)

    data = ser.read(size=9)


    data_unpacked = struct.unpack('<xHHxxBB', data)
    pm25 = data_unpacked[0]/10
    pm10 = data_unpacked[1]/10

    if data[7] == (sum(data[1:7])) % 256:
        return([pm25, pm10])
    else:
        print("Checksum is not correct.")


if __name__ == "__main__":

    sensor_set_wake()
    time.sleep(5)
    ser.reset_input_buffer()

    pm = sensor_query_data()
    print("PM 2.5 = " + str(pm[0]) + " μg/m^3\nPM 10.0 = " + str(pm[1]) + " μg/m^3")

    sensor_set_sleep()
