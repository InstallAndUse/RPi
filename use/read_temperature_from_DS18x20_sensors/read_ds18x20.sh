#!/bin/bash
#
# history and doc, refer to read_ds18x20.py /A
#
# 2022 03 18  + published on https://github.com/InstallAndUse/RPi /A

host="(host)"
user="(user)"
export PGPASSWORD="(dbpass)";
db="(dbname)"
table="(dbtable)"

while read line                      # read values for each sensor
    do
        values=(${line//;/ })        # split by ";" and build array
        if [ -n "$values" ]; then    # if array is not empty (empty line) write to DB
            echo "INSERT INTO ${table} (timestamp, sensor, value) VALUES (NOW(),'${values[0]}','${values[1]}')" | psql -h ${host} -U ${user} -d ${db}
        fi
    done < "${1:-/dev/stdin}"        # read stdin from python script (read sensors)
