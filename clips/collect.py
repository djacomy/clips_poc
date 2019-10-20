import pandas as pd
import requests
import re,json,io
import json, os
import geopandas as gpd
from bs4 import BeautifulSoup as bsp

import shapely.wkb

# sqlite/spatialite
from sqlalchemy import create_engine, event
from sqlite3 import dbapi2 as sqlite

from .settings import SQLALCHEMY_DATABASE_URI

base_url = "https://umap.openstreetmap.fr/fr/"
umap_url = "{}/search/".format(base_url)
data_dir = os.path.join("data")


map_color_type = {'DarkCyan': "H",
                  'YellowGreen': "P",
                  'Grey': "P",
                  'DimGray': "P",
                  'Red': 'P',
                  'Chartreuse': 'P',
                  'OrangeRed': 'P',
                  'Aqua': "W",
                  'DarkBlue': "W",
                  'Salmon': "X"
                  }


def find_maps(soup):
    result = []
    for carto in soup.findAll("div", {"class": "map_fragment"}):
        m = re.search('"search_map\d*_\d+",\s(\{.*\})\);', carto.parent.script.text, re.MULTILINE)
        if not m:
            continue
        tmp = json.loads(m.group(1))
        print(carto.attrs["id"].split("_")[-1], tmp["properties"]["umap_id"], tmp["properties"]["name"],
              tmp["properties"]["datalayers"])
        result.append(tmp)
    return result


def get_geojson_map(datalayer_id, map_id, map_name):
    url1 = "{}/datalayer/{}/".format(base_url, datalayer_id)
    response = requests.get(url1)
    if response.status_code != 200:
        raise Exception("No response !")
    res = response.json()
    for f in res["features"]:
        if "description" not in f["properties"]:
            continue
        desc = f["properties"]["description"].split("#")
        options = f["properties"].get("_umap_options")
        if options:
            f["properties"]["energy"] = map_color_type[options.get('color', 'Grey')]
        if len(desc) < 9:
            continue
        f["properties"]["house_type"] = desc[1]
        f["properties"]["logement_count"] = desc[2]
        f["properties"]["p_panel_count"] = int(desc[3])
        f["properties"]["w_panel_count"] = int(desc[4])
        f["properties"]["north_azimut"] = int(desc[5] or 0)
        f["properties"]["roof_shape"] = float(desc[6].replace(",", "."))
        f["properties"]["sunchine"] = float(desc[7].replace(",", "."))
        f["properties"]["validation"] = desc[8]
        if len(desc) == 10:
            f["properties"]["comment"] = desc[9]

    res["_umap_options"]["map_id"] = map_id
    res["_umap_options"]["map_name"] = map_name

    return res


def get_maps():
    url = "{}?q=clips".format(umap_url)
    result = []
    while url:
        response = requests.get(url)

        soup = bsp(response.content)
        result += find_maps(soup)
        more = soup.findAll("a", {"class": "more_button"})
        if more:
            url = '{}{}'.format(umap_url, more[0].attrs["href"])
        else:
            url = None
    return result


def get_maps_df(result):
    maps = {r["properties"]["datalayers"][0]["id"]: {"map_id": r["properties"]["umap_id"],
                                                     "name": r["properties"]["name"]} for r in result}
    res = []
    for k, v in maps.items():
        response = get_geojson_map(k, v.get("map_id"), v.get("name"))
        full_path = os.path.join(data_dir, "{}.geojson".format(v.get("name").replace("/", "").replace(" ", "_")))
        with open(full_path, "w") as fp:
            json.dump(response, fp, indent=2)
        # Read the geolocalised data
        regions = gpd.read_file(full_path)
        # regions['energy'] = regions['_umap_options'].apply(lambda x: map_color_type[x.get('color', 'Grey')] if not pd.isnull(x) else None)
        # regions['color'] = regions['_umap_options'].apply(lambda x: x.get('color') if not pd.isnull(x) else None)
        regions['geom'] = regions["geometry"]
        regions['map'] = v.get("name")
        regions['map_id'] = v.get("map_id")
        regions['datalayers_id'] = k
        regions.crs = {'init': 'epsg:4326'}
        res.append(regions)
    return pd.concat(res)


def write_database(filepath="CLIPS_Vernon.geojson"):
    gdf = gpd.read_file(os.path.join(data_dir, filepath))
    gdf.drop("_umap_options", inplace=True, axis=1)

    # read shapefile into GeoDataFrame
    print('reading shapefile')

    # make sure that the database does not exist yet, otherwise it will be opened instead of overwritten which will
    # cause errors in this example
    if os.path.exists('TestDB.sqlite'):
        os.remove('TestDB.sqlite')

    # create database engine and create sqlite database
    engine = create_engine(SQLALCHEMY_DATABASE_URI, module=sqlite)

    # load spatialite extension for sqlite. make sure that mod_spatialite.dll is located in a folder that is in your
    # system path
    @event.listens_for(engine, 'connect')
    def connect(dbapi_connection, connection_rec):
        dbapi_connection.enable_load_extension(True)
        dbapi_connection.execute('SELECT load_extension("mod_spatialite")')

    # create spatialite metadata
    print('creating spatial metadata...')
    engine.execute("SELECT InitSpatialMetaData(1);")

    # convert all values from the geopandas geometry column into their well-known-binary representations
    gdf['geometry'] = gdf.apply(lambda x: shapely.wkb.dumps(x.geometry), axis=1)

    # write the geodataframe into the spatialite database, creating a new table 'AddressPoints' and replacing any
    # existing of the same name
    print('writing into database...')
    gdf.to_sql('AddressPoints', engine, if_exists='replace', index=False)

    # add a Spatialite geometry column called 'geom' to the table, using ESPG 4326, data type POINT and 2 dimensions
    # (x, y)
    engine.execute("SELECT AddGeometryColumn('AddressPoints', 'geom', 4326, 'POINT', 2);")

    # update the yet empty geom column by parsing the well-known-binary objects from the geometry column into
    # Spatialite geometry objects
    engine.execute("UPDATE AddressPoints SET geom=GeomFromWKB(geometry, 4326);")


def read_database():
    # create database engine and open existing sqlite database
    engine = create_engine(SQLALCHEMY_DATABASE_URI, module=sqlite)

    # load spatialite extension for sqlite. make sure that mod_spatialite.dll is located in a folder that is in your
    # system path
    @event.listens_for(engine, 'connect')
    def connect(dbapi_connection, connection_rec):
        dbapi_connection.enable_load_extension(True)
        dbapi_connection.execute('SELECT load_extension("mod_spatialite")')

    # select X and Y coordinates from the POINT geometries in the database table
    x = engine.execute("SELECT X(geom) FROM AddressPoints;")
    y = engine.execute("SELECT Y(geom) FROM AddressPoints;")

    # print results
    xy = zip(x, y)
    for row in xy:
        print(row)
