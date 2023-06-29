#
# Objective: to connect to internal resources
#
#
# 2023-03-13  * second deployment, reviewed and updated /A


Official documentation is located here:
https://goteleport.com/docs/deploy-a-cluster/open-source/

# utils needed, but not mandatory
```
apt install tmux
```

# Host-based firewall, port forwardings in routers
open (80,443)/tcp to access Teleport and let CertBot to verify domain (it will start webserver for validation)


# get certbot running with Let's Encrypt first
```
apt install certbot
certbot certonly --standalone -d (domain) --staple-ocsp -m (host)-certbot@(domain) --agree-tos
```
to test cert renewal:
```
certbot renew --dry-run
```


# run webserver test
```
nano demo-app/index.html
python3 -m http.server 9000 --directory demo-app
```

# Downloading and installing
determine which architecture in use (I got on my RPi3)
```
getconf LONG_BIT
32
uname -a
Linux (host) 5.15.84-v7+ #1613 SMP Thu Jan 5 11:59:48 GMT 2023 armv7l GNU/Linux
```
download from original source, upload to destination and install package from (choose Linux in Top-Right corner)
https://goteleport.com/download/#install-links
or download directly from host
```
wget https://cdn.teleport.dev/teleport_12.1.0_arm.deb
dpkg -i ./teleport_12.1.0_arm.deb
```
? possible dependecies fix, if needed
```
apt-get -f install
```


# Configuration
set variable by executing commands and launch configuration tool
```
DOMAIN=(domain)
EMAIL=(host)-teleport@(domain)
teleport configure --acme --acme-email=${EMAIL?} --cluster-name=${DOMAIN?} | tee /etc/teleport.yaml > /dev/null
```
Add web-based frontend for Teleport by editing config file
```
nano /etc/teleport.yaml
app_service:
  enabled: yes
  apps:
  - name: "demo"
    uri: "http://localhost:9000"
    public_addr: "(domain)"
```


# enable and start the service
```
systemctl enable teleport
systemctl restart teleport
systemctl status teleport
```


# Configuring via WebUi (at this point, it should be accessible)
URL should look like something like this:
https://(domain)/web/login?redirect_uri=https://(domain)/web


# create admin user and set pass (list usernames, which user can represent (='login as'))
```
tctl users add teleport-admin --roles=editor,access --logins=root,ubuntu,ec2-user
User "teleport-admin" has been created but requires a password. Share this URL with the user to complete user setup, link is valid for 1h:
https://(domain):443/web/invite/953f9ea8c84c???????8f630874638c

NOTE: Make sure (domain):443 points at a Teleport proxy which users can access (networking works properly).
```
open link in browser and set pass for created user (it is supposed to send this link to end-user)
QR code of OTP token will be generated, use any token management (authentication application) to store it and provide OTP to finalize registration


# connecting via WebUI
choose "server", [connect] and choose which user to use as login (Teleport instance should be visible)


# creating normal users (father-mother-sister-brother) with access role only
tctl users add (user) --roles=access --logins=(user)





# adding new resource - server
it is not possible to deploy Teleport as a resource to itself
from WebUi, Servers > Add Server > Server [Next], copy-paste shell command and execute it on destination (new) server.
looks like, access to internet is needed to: https://get.gravitational.com/
```

root@(host):/home/(user)# bash -c "$(curl -fsSL https://(domain)/scripts/c1f0d3d9c6617773a230f89795b40a08/install-node.sh)"
2022-12-05 08:01:00 GMT [teleport-installer] TELEPORT_VERSION: 11.1.1
2022-12-05 08:01:00 GMT [teleport-installer] TARGET_HOSTNAME: (domain)
2022-12-05 08:01:00 GMT [teleport-installer] TARGET_PORT: 443
2022-12-05 08:01:00 GMT [teleport-installer] JOIN_TOKEN: c1f0d3d9c6617773a230f89795b40a08
2022-12-05 08:01:00 GMT [teleport-installer] CA_PIN_HASHES: sha256:94aa8871de87837e5a936f1963d4c6baf21a22031af87637122fcc636211e210
2022-12-05 08:01:00 GMT [teleport-installer] Checking TCP connectivity to Teleport server ((domain):443)
2022-12-05 08:01:00 GMT [teleport-installer] Connectivity to Teleport server (via nc) looks good
2022-12-05 08:01:00 GMT [teleport-installer] Detected host: linux-gnueabihf, using Teleport binary type linux
2022-12-05 08:01:01 GMT [teleport-installer] Detected arch: armv7l, using Teleport arch arm
2022-12-05 08:01:01 GMT [teleport-installer] Detected distro type: debian
2022-12-05 08:01:01 GMT [teleport-installer] Using Teleport distribution: deb
2022-12-05 08:01:01 GMT [teleport-installer] Created temp dir /tmp/teleport-Fol7L1QOSH
2022-12-05 08:01:01 GMT [teleport-installer] Downloading Teleport deb release 11.1.1
2022-12-05 08:01:01 GMT [teleport-installer] Running curl -fsSL --retry 5 --retry-delay 5 https://get.gravitational.com/teleport_11.1.1_arm.deb
2022-12-05 08:01:01 GMT [teleport-installer] Downloading to /tmp/teleport-Fol7L1QOSH/teleport_11.1.1_arm.deb
2022-12-05 08:01:57 GMT [teleport-installer] Downloaded file size: 103483964 bytes
2022-12-05 08:01:57 GMT [teleport-installer] Will use shasum -a 256 to validate the checksum of the downloaded file
[...]
2022-12-05 08:02:01 GMT [teleport-installer] The downloaded file's checksum validated correctly
2022-12-05 08:02:01 GMT [teleport-installer] Using dpkg to install /tmp/teleport-Fol7L1QOSH/teleport_11.1.1_arm.deb
Selecting previously unselected package teleport.
(Reading database ... 43613 files and directories currently installed.)
Preparing to unpack .../teleport_11.1.1_arm.deb ...
Unpacking teleport (11.1.1) ...
Setting up teleport (11.1.1) ...
2022-12-05 08:03:05 GMT [teleport-installer] Found: Teleport v11.1.1 git:v11.1.1-0-gbf4e8ea41 go1.19.2
2022-12-05 08:03:05 GMT [teleport-installer] Writing Teleport node service config to /etc/teleport.yaml

A Teleport configuration file has been created at "/etc/teleport.yaml".
To start Teleport with this configuration file, run:

sudo teleport start --config="/etc/teleport.yaml"

Note that starting a Teleport server with this configuration will require root access as:
- The Teleport configuration is located at "/etc/teleport.yaml".
- Teleport will be storing data at "/var/lib/teleport". To change that, run "teleport configure" with the "--data-dir" flag.

Happy Teleporting!
2022-12-05 08:03:06 GMT [teleport-installer] Host is using systemd
2022-12-05 08:03:06 GMT [teleport-installer] Starting Teleport via systemd. It will automatically be started whenever the system reboots.
Created symlink /etc/systemd/system/multi-user.target.wants/teleport.service → /lib/systemd/system/teleport.service.

Teleport has been started.

View its status with 'sudo systemctl status teleport.service'
View Teleport logs using 'sudo journalctl -u teleport.service'
To stop Teleport, run 'sudo systemctl stop teleport.service'
To start Teleport again if you stop it, run 'sudo systemctl start teleport.service'

You can see this node connected in the Teleport web UI or 'tsh ls' with the name '(host)'
Find more details on how to use Teleport here: https://goteleport.com/docs/user-manual/
```
service may be checked with
```
root@(host):/home/(user)# systemctl status teleport
```
and in WebUI below message will appear:
```
The server successfully joined this Teleport cluster
```
click [Next], choose OS users, who can connect to new server.
choose which OS user to test connection
```
Step 2
Verify that the server is accessible
Testing complete
You have access to the Node.
Node is alive and reachable.
The requested principal is allowed.
"(user)" user exists in target node
```
you may test a session by connecting directly from WebUI by pressing [Test session]

Finally, press [Finish]. New server will appear in the list.





# connecting using tsh (Teleport SSH)
download and install tsh client from:
https://goteleport.com/download/?os=mac
reopen terminal to be able to find 'tsh' command
```
(user)@(local) ~ % tsh login --proxy=(domain) --user=(local)
Enter password for Teleport user anton:
Enter your OTP token:
> Profile URL:        https://(local):443
  Logged in as:       (user)
  Cluster:            (domain)
  Roles:              access
  Logins:             (user), -teleport-internal-join
  Kubernetes:         enabled
  Valid until:        2023-03-14 05:58:00 +0300 +03 [valid for 12h0m0s]
  Extensions:         login-ip, permit-agent-forwarding, permit-port-forwarding, permit-pty, private-key-policy
  ```





# list and connect to the new server
```
tsh ls
Node Name Address        Labels
--------- -------------- ----------------
(host)   127.0.0.1:3022 hostname=(host)
tsh ssh (user)@(host)
```




# Download Desktop Clients (Teleport Connect), if needed (graphical interfaces):
https://goteleport.com/download/#install-links