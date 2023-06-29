#
# 2020 06 12  + init /A
# 2022 03 18  + published on https://github.com/InstallAndUse/RPi /A
#


# INSTALLATION:

 sudo su
# raspi-config, 5. interfaceing, P7 1-wire, enable, yes. reboot
 ls -la /sys/bus/w1/devices/*
     lrwxrwxrwx 1 root root 0 Jun 12 12:18 /sys/bus/w1/devices/00-200000000000 -> ../../../devices/w1_bus_master1/00-200000000000
     lrwxrwxrwx 1 root root 0 Jun 12 12:18 /sys/bus/w1/devices/00-a00000000000 -> ../../../devices/w1_bus_master1/00-a00000000000
     lrwxrwxrwx 1 root root 0 Jun 12 12:13 /sys/bus/w1/devices/w1_bus_master1 -> ../../../devices/w1_bus_master1#


# when sensors connected:
# (connect VCC to 5V, GND to GND, DATA to TXD PIN, remember to put resistor 4.7 kOhm between VCC and DATA)
 ls -la /sys/bus/w1/devices/*
     lrwxrwxrwx 1 root root 0 Jun 12 12:20 /sys/bus/w1/devices/00-600000000000 -> ../../../devices/w1_bus_master1/00-600000000000
     lrwxrwxrwx 1 root root 0 Jun 12 12:20 /sys/bus/w1/devices/00-e00000000000 -> ../../../devices/w1_bus_master1/00-e00000000000
     lrwxrwxrwx 1 root root 0 Jun 12 12:20 /sys/bus/w1/devices/10-000800e489b3 -> ../../../devices/w1_bus_master1/10-000800e489b3   <-- this is first sensor
     lrwxrwxrwx 1 root root 0 Jun 12 12:20 /sys/bus/w1/devices/10-00080280a759 -> ../../../devices/w1_bus_master1/10-00080280a759   <-- this is second sensor
     lrwxrwxrwx 1 root root 0 Jun 12 12:18 /sys/bus/w1/devices/w1_bus_master1 -> ../../../devices/w1_bus_master1#


# save this script (read_ds18x20.py) and bash script (read_ds18x20.psh) to /home/pi/meter
 chmod +x /home/pi/meter/*
 ls -la /home/pi/meter/*


# check you have python installed (probabaly on RPi it is)
 which python
     /usr/bin/python

# eventually, run first read
 root@(host):/home/pi/meter# ./read_ds18x20.py
     /sys/bus/w1/devices/10-000800e489b3;27000
     /sys/bus/w1/devices/10-00080280a759;29500#


# prepare PostgreSQL database for telemetry gathering (satellite)
#

# install postgres
sudo su
apt install postgresql

# start cluster
pg_ctlcluster 11 main start

# connect to DB
su - postgres
psql

# create user (user is named accordingly to hostname to simplicity in future replication configuration)
CREATE USER (user) WITH PASSWORD '(pass)';
\du

# create database (there is only one DB named telemetry to avoid confusion)
CREATE DATABASE telemetry;
\l

# grant access to (user)
GRANT ALL ON DATABASE telemetry TO (user) ;
\l telemetry

# connect to DB and create table
# tables are named individually to keep order for replication
# telemetry_hostname represents table with telemetry for hostname
\c telemetry
CREATE TABLE telemetry_host();
\d
\d telemetry_host

# adding columns to table
# it is importnant to set NOT NULL, because we do not want to keep DB clean and tidy
ALTER TABLE telemetry_host ADD COLUMN timestamp TIMESTAMPTZ PRIMARY KEY;
ALTER TABLE telemetry_host ADD COLUMN sensor CHAR(64) NOT NULL;
ALTER TABLE telemetry_host ADD COLUMN value INTEGER NOT NULL;
\d telemetry_host

# grant access on table to (user)
???



# change DB credentials in shell script (user) and (pass)
 nano ./read_ds18x20.sh
 pi@(host):~/meter $ ./read_ds18x20.py | ./read_ds18x20.sh
     INSERT 0 1
     INSERT 0 1


# set peiodic check with cron (good idea to setup cron for root, because future checks will be consolidated in one place)
 sudo
 crontab -e
     */1 * * * * /home/pi/meter/read_ds18x20.py | /home/pi/meter/read_ds18x20.sh


# check that cron is working:
 tail -f /var/log/syslog | grep CRON
     Jun 12 12:47:01 lab5rp41 CRON[1507]: (root) CMD (/home/pi/meter/read_ds18x20.py | /home/pi/meter/read_ds18x20.sh)
     Jun 12 12:47:04 lab5rp41 CRON[1503]: (CRON) info (No MTA installed, discarding output)#


# check that entries actually written to db
 psql -h (host_ip) -U (user2) -d (db) -c "SELECT * FROM telemetry_host;"
     Password for user (host):
                timestamp           | value |                              sensor
     -------------------------------+-------+------------------------------------------------------------------
      2020-06-12 08:58:36.732033+01 | 12345 | test_sensor
      2020-06-12 10:38:12.519066+01 | 27500 | /sys/bus/w1/devices/10-000800e489b3
      2020-06-12 10:38:12.68798+01  | 29000 | /sys/bus/w1/devices/10-00080280a759
      2020-06-12 10:38:47.060764+01 | 27000 | /sys/bus/w1/devices/10-000800e489b3
      2020-06-12 10:38:47.222548+01 | 28937 | /sys/bus/w1/devices/10-00080280a759
      2020-06-12 10:46:38.363432+01 | 27062 | /sys/bus/w1/devices/10-000800e489b3
      2020-06-12 10:46:38.552815+01 | 28812 | /sys/bus/w1/devices/10-00080280a759
      2020-06-12 10:47:03.880082+01 | 27687 | /sys/bus/w1/devices/10-000800e489b3
      2020-06-12 10:47:04.031554+01 | 28750 | /sys/bus/w1/devices/10-00080280a759
     (9 rows)



Books:
- [Anton's bookshelf](https://og2k.com/books/)
