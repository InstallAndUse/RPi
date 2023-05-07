#
# Configuring VPN server on Raspberry Pi
#

# 2022-09-07  + merged with installation logic in general /A
# 2023-01-20  * reviewed due to reinstallation /A
# 2023-03-12  * reinstalling, reviewing /A

# download recent Raspberry Pi OS Lite image and burn it to flash card [link]

# install recent Raspberry Pi Lite (without GUI interface) [link]

# configure firstboot [RPi/install_firstboot]

# configure manual IP address [link] (for port forwarding from router to VPN server)

# configure Dynamic DNS to ensure that VPN server is reachable, in case IP address changes [link]


# download PiVPN installer and execute
```
cd
sudo su
apt install curl
curl -L https://install.pivpn.io > installer.sh
chmod +x ./installer.sh
./installer.sh
```


# PiVPN can configured in two ways:
WireGuard and OpenVPN (differnce in protocol and listening port), clients' configuration is almost the same for both. Check which will work for you. Depends on your geographical location and locations you intended to connect from.


# unattended updates
Good idea, if system will stay long time alone.
Not so good idea, because of lack of control (inspection), which packages will be updated

reboot

login into local user, which is holding pivpn configuration files


# VPN Clients (*.ovpn files)
list and add VPN clients (users) "father-mother-sister-brother"
```
pivpn list
pivpn add
    Name: (client)
    How many days should the certificate last? [1080]
    Password: (pass)
```
now new user should be in the list and opvn config generated and can be found
```
pivpn list
ls -la /home/(user)/ovpns/
cat /home/(user)/ovpns/(client).ovpn
```


# Config files
You can copy config file in any desired way (scp probably is the best).
Or cat it and copy-paste.
Or generate QR-code for WireGuard Android's application (is not available for OpenConnect)
```
pivpn -qr
```


# troubleshooting
```
netstat -ntap
netstat -p | grep openvpn
systemctl status openvpn
iptables -L -n -v --line-numbers
```


# to fix broken IP forwarding, run command below and follow instructions
```
pivpn debug
```


mkdir -p /etc/openvpn/easy-rsa/pki/
/usr/sbin/openvpn --genkey secret /etc/openvpn/easy-rsa/pki/ta.key
? /usr/sbin/openvpn --genkey secret /etc/openvpn/ta.key
? /usr/sbin/openvpn --genkey secret /etc/openvpn/easy-rsa/keys/ta.key



# source https://docs.pivpn.io/install/





Books:
- [Anton's bookshelf](https://og2k.com/books/)
