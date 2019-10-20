# clips_poc

SAAS platform to decrease carbon in the use of electricity

## Pre-requisite

Install spatialite for Sqlite 3

```
apt-get install -y --no-install-recommends sqlite3 libsqlite3-mod-spatialite
```


## Initalize Sqlite Database


```
python manage.py crawl
```

## Launch server

- Copy .env.template to .env 
- Fill the MAPBOX_ACCESS_KEY with your account
- Launch the script start.sh





