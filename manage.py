import argparse
import os
from clips.commands import crawl

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="actions")

    crawl_cmd = subparsers.add_parser("crawl", description=f'crawl data')
    crawl_cmd.set_defaults(func=crawl)

    args = parser.parse_args()
    arguments = args.__dict__
    func = arguments.pop('func', None)
    if not func:
        os._exit(-1)
    func(**arguments)
