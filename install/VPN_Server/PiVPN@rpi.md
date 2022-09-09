#
# Configuring VPN server on Raspberry Pi
#

# 2022-09-07  + merged with installation logic in general


# source https://docs.pivpn.io/install/

# download recent Raspberry Pi OS Lite image and burn it to flash card [link]

# install recent Raspberry Pi Lite (without GUI interface) [link]

# configure firstboot [RPi/install_firstboot]

# configure manual IP address [link] (for port forwarding from router to VPN server)

# configure Dynamic DNS to ensure that VPN server is reachable, in case IP address changes [link]

# download PiVPN installer and execute
```
sudo su
curl -L https://install.pivpn.io > installer.sh
chmod +x installer.sh
./installer.sh
```


# unattended updates
Good idea, if system will stay long time alone.
Not so good idea, because of lack of control (inspection), which packages will be updated

reboot

login into local user, which is holding pivpn configuration files

# VPN Clients
list and add
```
pivpn list
pivpn add
    Name: (client)
    How many days should the certificate last? [1080]
    Password: (pass)
```
now new user should be in the list and opvn config generated and can be found
```
ls -la /home/(config user)/ovpns/
(client).ovpn
```

# Config files
You can copy config file in any desired way (scp probably is the best).

Or generate QR-code for WireGuard Android's application
```
pivpn -qr
```




Books:
- [Anton's bookshelf](https://og2k.com/books/)
