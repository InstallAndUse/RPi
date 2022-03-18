#!/usr/bin/python
#
# read DS18b20 or DS1820 sensors
#
# 2020 05 07  * initial code for DS18B20 /A
# 2020 05 08  + multi sensor support /A
#             + DS1820 support /A
#             * return in millidegrees (get rid of float)
# 2020 06 12  + install doc added /A
# 2022 03 18  + published on https://github.com/InstallAndUse/RPi /A
#             * moved doc to separate README.md file /A
#


#
# TODO:
#
#



import glob

base_dir = '/sys/bus/w1/devices/'
sensors = glob.glob(base_dir + '[28|10]*')
for sensor in sensors:
    f = open(sensor + '/w1_slave', 'r')
    lines = f.readlines()
    f.close()
    if lines[0].strip()[-3:] == 'YES':
        value = lines[1][lines[1].find('t=')+2:]
    print("%s;%s" %(sensor, value))
