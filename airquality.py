#!/usr/bin/env python3
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "Jyf"

import datetime
import time

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_air_quality import BrickletAirQuality
from influxdb import InfluxDBClient

now = 0
json_body = []
influx_args=('localhost', 8086, 'root', '', 'tinkerforge')
dbclient = InfluxDBClient(*influx_args)


if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    aq = BrickletAirQuality(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Get current all values
    iaq_index, iaq_index_accuracy, temperature, humidity, \
      air_pressure = aq.get_all_values()

    print("IAQ Index: " + str(iaq_index))
    iaq = str(iaq_index)

    if iaq_index_accuracy == aq.ACCURACY_UNRELIABLE:
        print("IAQ Index Accuracy: Unreliable"),
        iaq_accuracy = "Unreliable"
    elif iaq_index_accuracy == aq.ACCURACY_LOW:
        print("IAQ Index Accuracy: Low"),
        iaq_accuracy = "Low"
    elif iaq_index_accuracy == aq.ACCURACY_MEDIUM:
        print("IAQ Index Accuracy: Medium"),
        iaq_accuracy = "Medium"
    elif iaq_index_accuracy == aq.ACCURACY_HIGH:
        print("IAQ Index Accuracy: High"),
        iaq_accuracy = "High"

    print("Temperature: " + str(temperature/100.0) + " °C")
    temp = str(temperature/100.0)
    print("Humidity: " + str(humidity/100.0) + " %RH")
    humidity = str(humidity/100.0)
    print("Air Pressure: " + str(air_pressure/100.0) + " hPa")
    airpressure = str(air_pressure/100.0)

    ts = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    json_body.append(
       {
           "measurement": "monitor_reading",
               "tags": {
                       "bricklet": UID
               },
               "time": ts,
               "fields": {
                       "iaq": int(iaq),
                       "iaq_accuracy": iaq_accuracy,
                       "temperature": float(temp),
                       "humidity": float(humidity),
                       "airpressure": float(airpressure)
          }
    })

    print (json_body)
    dbclient.write_points(json_body)

    ipcon.disconnect()


# IAQ Index: 237
# IAQ Index Accuracy: High
# Temperature: 25.71 °C
# Humidity: 55.72 %RH
# Air Pressure: 1005.96 hPa
