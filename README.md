# clips_poc

SAAS platform to decrease carbon in the use of electricity

## Pre-requisite

Generate locale
```
locale-gen en_US.UTF-8
export LANG=en_US.UTF-8 LANGUAGE=en_US.en LC_ALL=en_US.UTF-8
```

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





