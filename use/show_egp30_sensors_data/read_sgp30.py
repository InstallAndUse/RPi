#!/usr/bin/python3
#
# read sgp30 sensor
#
# 2020 05 19  * init  /A
# 2022 03 19  + published on https://github.com/InstallAndUse/RPi /A
#
# TODO:
#
#

import busio
import adafruit_sgp30

import board
i2c_bus = busio.I2C(board.SCL, board.SDA, frequency=1000000)

sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c_bus)

print("SGP30 serial #", [hex(i) for i in sgp30.serial])

eCO2, TVOC = sgp30.iaq_measure()
print("eCO2 = %d ppm \t TVOC = %d ppb" % (eCO2, TVOC))
