# Configuring static IP on Raspberry Pi (ethernet/eth0/LAN)


```
nano /etc/dhcpcd.conf

interface eth0
static ip_address=192.168.72.8/24
static_routers=192.168.72.1
static domain_name_servers=192.168.72.1


```

Restart with caution, remember, your IP will be changed:
```
shutdown -r now
```



Clean old key with:
```
ssh-keygen -R 192.168.72.195
```