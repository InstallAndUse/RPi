#
# 2020 05 27  + init RTC@rpi  /A
# 2022 03 19  + published on https://github.com/InstallAndUse/RPi /A
#

# enable modules
sudo
nano /etc/modules
    i2c-bcm2708
    i2c-dev

nano /etc/modprobe.d/raspi-blacklist.conf
# comment
# blacklist spi-bcm2708
# blacklist i2c-bcm2708

#
# SPI (DS1302)
#


#
# i2c (DS1307, PCF8523, DS3231)
#
apt install i2c-tools
i2cdetect -y 1
modprobe rtc-ds1307
echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device

# read RTC
hwclock -r

# write RTC
hwclock -w


# add to boot
nano /etc/init.d/hwlock.sh
# unset TZ at top add
    do
      echo ds1307 0x68 >> $bus/new_device;
      if [ -e /dev/rtc0 ];
      then
        log_action_msg "RTC found on bus `cat $bus/name`";
        break; # RTC found, bail out of the loop
      else
        echo 0x68 >> $bus/delete_device
      fi
    done
    }
# near case, chage
    case "$1" in
    	start)
    	    # If the admin deleted the hwclock config, create a blank
    	    # template with the defaults.
    	    if [ -w /etc ] && [ ! -f /etc/adjtime ] && [ ! -e /etc/adjtime ]; then
    	        printf "0.0 0 0.0\n0\nUTC" > /etc/adjtime
    	    fi
    		init_rtc_device

                # Raspberry Pi doesn't have udev detectable RTC
    	    #if [ -d /run/udev ] || [ -d /dev/.udev ]; then

update-rc.d hwclock.sh enable
update-rc.d fake-hwclock remove

# remove fake hardware clock, used in RPi
sudo su
apt-get -y remove fake-hwclock
update-rc.d -f fake-hwclock remove
systemctl disable fake-hwclock










# refs:
# https://cdn-learn.adafruit.com/downloads/pdf/adding-a-real-time-clock-to-raspberry-pi.pdf



Books:
- [Anton's bookshelf](https://og2k.com/books/)



Books:
- [Anton's bookshelf](https://og2k.com/books/)
