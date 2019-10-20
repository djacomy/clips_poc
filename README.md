# clips_poc

SAAS platform whose goal is to build micro-networks of energy communities 
in urban or semi-urban areas; to locally produce electricity to be consumed 
within a radius of one kilometer or close.

POC build during the hackaton NextEra Energy Satellite Hack from the 
1st october 2019 to the 21st october 2019. (https://www.hackerearth.com/fr/challenges/hackathon/nextera-hackathon/)

## Our dream

Our dream is to be a trusted third party for all local stakeholders: 
local authorities, energy companies, facility owners, future installers or 
consumers for a local energy exchange system.

## What we want to build: 

We want to build these communities by satellite identification of solar 
power points on buildings or houses. Photovoltaic solar installations 
or hot water on the roofs of individual houses are our priority targets: 
  - photovoltaic installations to sell or buy solar energy according 
     to their needs versus their production, 
  - hot water production facilities may be interested in 
     completing their installation with photovoltaic panels or in 
     purchasing locally produced green or solar electricity.

## Roadmap: 

### POC (This version)

- Make cartographies in France of the Parisian cities (Grand Paris Seine and Oise, 
Vernon, Palaiseau, Saclay, etc.) via umap and import markers in our database.
- Provide the meam to see cartographies by cities for any consumer. 

### V1

- Create a register page to onboard on the project as consumer, producter and 
  Cities autorities. 
- Create a consumer dashboard to view how green is this house area
- Create a producter and Cities autorities dashord to pick on the map their 
  production site and provide characteristic data. 
  
### V2

- Perform the consumer page to be able to program behavior update's in order to
  affect the carbon rate in electricity consumption. 
- Add a mobile version of the application. 
  
### V3

- With data collected and satellite image, help to recogize production site. 


### V4
 
-  develop an electric price block chain. 


## Installation

### Pre-requisite

- Generate locale
```
locale-gen en_US.UTF-8
export LANG=en_US.UTF-8 LANGUAGE=en_US.en LC_ALL=en_US.UTF-8
```

- Install python3 and virtualenv

```
apt-get install -y --no-install-recommends python3 python-virtualenv
```

- Install spatialite for Sqlite 3

```
apt-get install -y --no-install-recommends sqlite3 libsqlite3-mod-spatialite
```

- Create virtualenv

```
mkdir .env && virtualenv -p python3 .env && . .env/bin/activate
```

- Install requirements

```
pip install -r requirements.txt
```

### Initalize Sqlite Database

```
python manage.py init-db
python manage.py migrate 20191020_create_marker.sql
```

### Crawl markers

```
python manage.py crawl 
```

### Import markers

```
python manage.py import-marker CLIPS_Vernon.geojson 

```


### Launch server

- Copy .env.template to .env 
- Fill the MAPBOX_ACCESS_KEY with your account
- Launch the script start.sh





