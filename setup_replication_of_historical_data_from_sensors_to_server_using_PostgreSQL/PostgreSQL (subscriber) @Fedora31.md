2020 05 26

https://www.scalingpostgres.com/tutorials/
https://www.percona.com/blog/2018/09/07/setting-up-streaming-replication-postgresql/
https://www.howtoforge.com/tutorial/postgresql-replication-on-ubuntu-15-04/
https://blog.raveland.org/post/postgresql_lr_en/
https://blog.dbi-services.com/in-core-logical-replication-will-hit-postgresql-10/
https://debezium.io/documentation/reference/postgres-plugins.html
https://paquier.xyz/postgresql-2/postgres-9-4-feature-highlight-basics-logical-decoding/


# install server
yum install postgresql-server
/usr/bin/postgresql-setup --initdb


# make sure local cluster exist
su - postgres
pg_ctl -D /var/lib/pgsql/data/10-main initdb
pg_ctl -D /var/lib/pgsql/data/10-main -l logfile start


# create a cluster for replica
su - postgres
pg_ctl -D /var/lib/pgsql/data/20-replica-lab5rpz1 initdb

# run and test
pg_ctl -D /var/lib/pgsql/data/20-replica-lab5rpz1 start -l logfile
psql -p 5433 postgres
C-C

# ensure, that correct DB is started as service
systemctl enable postgresql
nano /usr/lib/systemd/system/postgresql.service
    Environment=PGDATA=/var/lib/pgsql/data/10-main
systemctl daemon-reload
systemctl start postgresql

# check replication status
psql
# expect logical
SHOW wal_level;

# create identical table as on publisher
CREATE TABLE ...

# create subscription for first satellite
# with IP
CREATE SUBSCRIPTION lab5rpz1_main CONNECTION 'host=192.168.7.134 port=5432 user=(user2) password=123 dbname=postgres' PUBLICATION main;
# then I realized, it is possible to use hostname, which will be resolved over network, in case IP address will change. Genius. :)
ALTER  SUBSCRIPTION lab5rpz1_main CONNECTION 'host=lab5rpz1      port=5432 user=(user2) password=123 dbname=postgres';

# second satellite
CREATE TABLE telemetry_lab5rp41;
CREATE SUBSCRIPTION telemetry_lab5rp41 CONNECTION 'host=lab5rp41 port=5432 user=(user2) password=(user2)123 dbname=telemetry' PUBLICATION telemetry_lab5rp41;
GRANT ALL ON TABLE telemetry_lab5rp41 TO (user2) ;


# check replication
SELECT * FROM pg_stat_replication;
