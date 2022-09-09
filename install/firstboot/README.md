#
# initial Raspberry Pi configuration
#
# 2020 06 12  + init of firstboot@rpi.md /A
# 2022 03 19  + published on https://github.com/InstallAndUse/RPi /A
#

# set pi pass
passwd

# set root pass
sudo su
passwd

# add yourself (for ssh keys, security. etc...)
useradd (you)
passwd (you)
usermod -aG sudo (you)
mkdir /home/(you)
chown -R (you):(you) /home/(you)

# update, reboot and run update one more time
```
apt update && apt upgrade -y
shutdown -r now
apt update && apt upgrade -y
```

# initial config
raspi-config
2. N1, set hostname
4. localisation, I2, set timezone
5. interfacing, P2, enable ssh

# reboot




Books:
- [Anton's bookshelf](https://og2k.com/books/)
