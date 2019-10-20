import argparse
import sys
from clips.commands import init_db, crawl, migration, import_markers

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="actions")

    init_db_cmd = subparsers.add_parser("init-db", description=f'Initialize spatial database.')
    init_db_cmd.set_defaults(func=init_db)

    crawl_cmd = subparsers.add_parser("crawl", description=f'crawl data')
    crawl_cmd.set_defaults(func=crawl)

    import_cmd = subparsers.add_parser("import-marker", description=f'Import markers from geojson.')
    import_cmd.add_argument("filename", action="store")
    import_cmd.add_argument("libelle", action="store")
    import_cmd.set_defaults(func=import_markers)

    mig_cmd = subparsers.add_parser("migrate", description=f'Migration command.')
    mig_cmd.add_argument("filename", action="store")
    mig_cmd.set_defaults(func=migration)

    args = parser.parse_args()
    arguments = args.__dict__
    func = arguments.pop('func', None)
    if not func:
        sys.exit(-1)
    func(**arguments)
