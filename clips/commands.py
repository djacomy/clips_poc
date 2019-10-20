import os
from .collect import get_maps, get_maps_df, write_database
from .database import engine
from .settings import PROJECT_ROOT


def crawl():

    result = get_maps()
    get_maps_df(result)


def import_markers(filename):
    if not filename.endswith(".geojson"):
        raise ValueError("Bad Format")

    if not os.path.exists(os.path.join("data", filename)):
        raise ValueError(f"{filename} not exit -> please crawl!")

    write_database(filename)


def init_db():

    # make sure that the database does not exist yet, otherwise it will be opened instead of overwritten which will
    # cause errors in this example
    if os.path.exists('TestDB.sqlite'):
        os.remove('TestDB.sqlite')

    # create spatialite metadata
    print('creating spatial metadata...')
    engine.execute("SELECT InitSpatialMetaData(1);")


def migration(filename):
    file_path = os.path.join(PROJECT_ROOT, "sql", "migrations", filename)
    if not os.path.exists(file_path):
        raise Exception("Unknown script")

    with open(file_path, "r") as fp:
        sql_cmd = fp.read()

    connection = engine.connect()

    with connection.begin() as trans:
        connection.execute("BEGIN TRANSACTION;")
        connection.execute(sql_cmd)
        trans.commit()
