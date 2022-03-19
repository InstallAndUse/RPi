# In this project we shall setup NTP-server on Raspberry using GPS-receiver connected to serial port.
#
# 2020 05 26  + init chrony@rpi /A
# 2022 03 19  + published on https://github.com/InstallAndUse/RPi /A
#

# getting time from gps
apt install gpsd gpsd-clients python-gps
nano /etc/default/gpsd
    DEVICES="/dev/ttyAMA0"
    GPSD_OPTIONS="-n"
systemctl enable gpsd && systemctl restart gpsd
systemctl status gpsd
# add serial device (BT uses another one)
nano /boot/config.txt
    dtoverlay=pi3-miniuart-bt
    core_freq=250
shutdown -r now
# test
cgps -s
gpsmon -n


# setting up NTP server
apt install chrony
#? systemctl enable chronyd && systemctl restart chronyd
systemctl status chronyd
chronyc sources -v
nano /etc/chrony/chrony.conf
    # comment for setup, uncomment on finish (to keep for time comparison)
    pool 2.fedora.pool.ntp.org iburst
    pool 2.debian.pool.ntp.org iburst
    # add NMEA source as time reference
    refclock SHM 0 offset 0.5 delay 0.2 refid NMEA
systemctl restart chronyd
chronyc sources -v

# test
ntpshmmon


# set up NTP server
nano /etc/chrony/chrony.conf
    allow 192.168.0.0/16
systemctl restart chronyd
# test
chronyc
    clients
    serverstats


# clean and remove ntpdate
apt remove ntpdate









# Remove ntp-servers from
nano /etc/dhcp/dhclient.conf
    # remove "request ntp-servers"
    # remove "option ntp_servers"
rm
    /etc/dhcp/dhclient-exit-hooks.d/ntp
    /lib/dhcpcd/dhcpcd-hooks/50-ntp.conf
    /var/lib/ntp/ntp.conf.dhcp (might not exist)







#
# refs: https://gpsd.gitlab.io/gpsd/gpsd-time-service-howto.html#_feeding_chrony_from_gpsd
#       http://www.unixwiz.net/techtips/raspberry-pi3-gps-time.html
