# create db with admin user.
```sh
read -p "Enter username: " username && read -p "Enter database name: " db_name && read -s -p "Enter password: " password && echo && createdb $db_name && psql -c "CREATE USER $username WITH PASSWORD '$password';" && psql -c "GRANT ALL PRIVILEGES ON DATABASE $db_name TO $username;" && psql -c "ALTER USER $username WITH SUPERUSER;"
```

# create user
su - postgres
createdb dbname
psql
CREATE USER admin WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE dbname to admin;


########## remote access
nvim /etc/postgresql/9.5/main/pg_hba.conf
host    all             all              0.0.0.0/0             md5

nvim /etc/postgresql/9.5/main/postgresql.conf
listen_addresses = '*'

systemctl restart postgresql


######### connect remote
psql -h hostname -U admin -d dbname

##### export
psql dbname > dbname.sql


## readonly user
psql
\c dbname;

CREATE ROLE viewer;

# grant permissions
GRANT CONNECT ON DATABASE refactored TO viewer;
GRANT USAGE ON SCHEMA public TO viewer;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO viewer;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO viewer;

# grant permissions for future tables
# Note that by default this will only affect objects (tables) created by the user that
issued this command
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO viewer;


# create child roles
CREATE ROLE dinesh WITH LOGIN PASSWORD 'password' NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION VALID UNTIL 'infinity';
grant viewer to dinesh;
