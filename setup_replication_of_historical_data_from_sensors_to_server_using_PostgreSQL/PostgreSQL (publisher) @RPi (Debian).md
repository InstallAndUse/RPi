# 2020 06 12  + init /A
# 2022 03 19  + published on https://github.com/InstallAndUse/RPi /A

# set publication (logical replication)
# first we need to create user who will be subscribed to this publication
# (again, to keep it simple, (user2) is a name of (host2) which will login)
CREATE USER (user2) WITH PASSWORD '(pass2)';
\du
CREATE PUBLICATION telemetry_host FOR TABLE telemetry_host;
SELECT * FROM pg_catalog.pg_publication;
\d telemetry_host

# grant readonly access on subscription to (user2)
ALTER ROLE (user2) REPLICATION ;
GRANT SELECT ON telemetry_host TO (user2);
\c telemetry
GRANT ALL ON TABLE public.telemetry_lab5rp41 TO lab5rp41 ;

# exit to console and insert into DB first entry
exit
psql -h localhost -U lab5rp41 -d telemetry -c "INSERT INTO telemetry_lab5rp41 (timestamp, sensor, value) VALUES (now(), 'test_sensor', '12345')"
    Password for user (user):
    INSERT 0 1

# check select with (user2)
psql -h localhost -U (user2) -d telemetry -c "SELECT * FROM telemetry_host"
    Password for user (user2):
               timestamp           | value |                              sensor
    -------------------------------+-------+------------------------------------------------------------------
     2020-06-12 08:58:36.732033+01 | 12345 | test_sensor
    (1 row)

# open access to database from network
# trying access DB to IP address (not to localhost), should denied access
ip a
psql -h (host_ip) -U (user2) -d telemetry -c "SELECT * FROM telemetry_host"
    psql: could not connect to server: Connection refused
      Is the server running on host "192.168.xxx.xxx" and accepting
      TCP/IP connections on port 5432?
# become root (logout postgres)
exit
sudo

# on moment of writing, configs for postgres on RPi are here, may differ for different linux distros
# enable listening on all interfaces
nano /etc/postgresql/11/main/postgresql.conf
    # - Connection Settings -
    listen_addresses = '*'
    wal_level = logical

# enable auth method
nano /etc/postgresql/11/main/pg_hba.conf
# we need to open network access for IPv4 and IPv6 (as RPi obtain IPv6 from DHCP as well)
# in this case, I am opening only access to DB telemetry and only for user (user2)
    # IPv4 local connections:
    host    all             all            127.0.0.1/32            md5
    host    replication     (user2)        0.0.0.0/0               md5
    host    telemetry       (user2)        0.0.0.0/0               md5
    # IPv6 local connections:
    host    all             all            ::1/128                 md5
    host    replication     (user2)        ::0/0                   md5
    host    telemetry       (user2)        ::0/0                   md5

# save, and restart postresql cluster
systemctl | grep sql
systemctl restart postgresql@11-main.service

# check that postgres is listening on network interfaces
netstat -ntap | grep 5432
    # postgres listens only on localhost
    tcp        0      0 127.0.0.1:5432          0.0.0.0:*               LISTEN      1796/postgres
    tcp6       0      0 ::1:5432                :::*                    LISTEN      1796/postgres

# now try again
psql -h (host_ip) -U (user2) -d telemetry -c "SELECT * FROM telemetry_host"
    Password for user lab5dle4:
               timestamp           | value |                              sensor
    -------------------------------+-------+------------------------------------------------------------------
     2020-06-12 08:58:36.732033+01 | 12345 | test_sensor
    (1 row)
# it is important to set it up correctly to this point to avoid confusion later on setting up subsciber-side

# open firewall, if needed for tcp/5432 (by default it is opened)
iptables -L -n -v --line-numbers | grep 5432


# reboot and retry last SELECT command, everything should work
