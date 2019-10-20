from sqlalchemy import create_engine, event
from sqlite3 import dbapi2 as sqlite

from .settings import SQLALCHEMY_DATABASE_URI, MAPBOX_ACCESS_KEY


engine = create_engine(SQLALCHEMY_DATABASE_URI, module=sqlite)

# load spatialite extension for sqlite. make sure that mod_spatialite.dll is located in a folder that is in your
# system path
@event.listens_for(engine, 'connect')
def connect(dbapi_connection, connection_rec):
    dbapi_connection.enable_load_extension(True)
    dbapi_connection.execute('SELECT load_extension("mod_spatialite")')
