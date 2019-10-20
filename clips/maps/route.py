from flask import Blueprint, render_template
from geojson import Feature, Point
import pandas as pd

from ..settings import MAPBOX_ACCESS_KEY
from ..database import engine

map_blueprint = Blueprint('map', __name__,  static_folder='../static')

# Landing Page


def df_to_geojson(df, properties, lat='lat', lon='lon'):
    geojson = {'type': 'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        feature = {'type': 'Feature',
                   'properties': {},
                   'geometry': {'type':'Point',
                               'coordinates': []}}
        feature['geometry']['coordinates'] = [row[lon], row[lat]]
        for prop in properties:
            feature['properties'][prop] = row.get(prop) or 'null'
        geojson['features'].append(feature)
    return geojson

def _format_title(row):
    field_map = {"P": {"name": "Adress",
                       "house_type": "House type",
                       "logement_count": "Flat count",
                       "p_panel_count": "Panel count",
                       "north_azimut": "North azimut",
                       "roof_shape": "Roof shape",
                       "sunchine": "Shunsine"},
                 "W": {"name": "Adress",
                       "house_type": "House type",
                       "logement_count": "Flat count",
                       "w_panel_count": "Panel count",
                       "north_azimut": "North azimut",
                       "roof_shape": "Roof shape",
                       "sunchine": "Shunsine"}
                 }

    nrj = row.get("energy") or "P"
    if nrj == "P":
        title =  "Energy: Photovoltaic<br />"
    else:
        title = "Energy: Solar hot water<br />"

    title += '<br />'.join([f"{v}: {row[k]}" for k, v in field_map[nrj].items()])
    return title


def create_markers(df):
    field_map = {"name": "Adress",
                 "energy": "Energy",
                 "house_type": "House type",
                 "logement_count": "Flat count",
                 "p_panel_count": "Photovoltaic panel count",
                 "w_panel_count": "Hot water panel count",
                 "north_azimut": "North azimut",
                 "roof_shape": "Roof shape",
                 "sunchine": "Shunsine"}
    stop_locations = []
    for _, row in df.iterrows():
        # Create a geojson object for stop location
        point = Point([row['lon'], row['lat']])

        properties = {
            'title': _format_title(row),
            'icon': 'campsite',
            'marker-color': '#3bb2d0',
            'marker-symbol': len(stop_locations) + 1
        }
        feature = Feature(geometry=point, properties=properties)
        stop_locations.append(feature)
    return stop_locations


@map_blueprint.route('/', methods=['GET'])
def mapbox_js():
    gdf = pd.read_sql("""SELECT lon, lat, name, energy, house_type, logement_count,
                         p_panel_count, w_panel_count, north_azimut, roof_shape,
                         sunchine, validation, comment 
                         FROM markers;""", engine)

    route_data = df_to_geojson(gdf, ['name', 'energy', 'house_type', 'logement_count'])
    markers = create_markers(gdf)

    return render_template(
        'maps/mapbox_js.html',
        ACCESS_KEY=MAPBOX_ACCESS_KEY,
        coords=[ gdf["lat"].median(), gdf["lon"].median()],
        route_data=route_data,
        markers=markers
    )
