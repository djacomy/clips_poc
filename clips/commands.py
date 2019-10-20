import os
from sqlalchemy import text
from .collect import get_maps, get_maps_df, write_database
from .database import engine
from .settings import PROJECT_ROOT


def crawl():

    result = get_maps()
    get_maps_df(result)


def import_markers(filename, libelle):
    if not filename.endswith(".geojson"):
        raise ValueError("Bad Format")

    if not os.path.exists(os.path.join("data", filename)):
        raise ValueError(f"{filename} not exit -> please crawl!")

    write_database(filename, libelle)


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
        sql_file = fp.read()

    connection = engine.connect()

    with connection.begin() as trans:
        connection.execute(text("BEGIN TRANSACTION;"))
        sql_command = ''
        for line in sql_file:
            # Ignore commented lines
            if line.startswith('--') or not line.strip('\n'):
                continue
            # Append line to the command string
            sql_command += line.strip('\n')

            # If the command string ends with ';', it is a full statement
            if sql_command.endswith(';'):
                # Try to execute statement and commit it
                try:
                    connection.execute(text(sql_command))

                # Assert in case of error
                except:
                    print('Ops')

                # Finally, clear command string
                finally:
                    sql_command = ''
        trans.commit()
