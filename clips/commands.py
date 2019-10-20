from .collect import get_maps, get_maps_df, write_database


def crawl():

    result = get_maps()
    get_maps_df(result)
    write_database()
