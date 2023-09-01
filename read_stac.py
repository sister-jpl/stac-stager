import json
import traceback
import argparse
from pystac import Catalog, get_stac_version
from pystac.extensions.eo import EOExtension
from pystac.extensions.label import LabelExtension
from urllib.request import urlretrieve


def main():
    """ 
    - Purpose: Outline details of STAC Catalog
    - Input: String of remote/local STAC catalog path 
    - Output: Print of Catalog ID, title, description, and items
    """ 
    # get args
    args = parser().parse_args()

    try: 
        if args.catalog[0]:
            # Read the example catalog
            root_catalog = Catalog.from_file(args.catalog[0])

            # Print some basic metadata from the Catalog
            print(f"ID: {root_catalog.id}")
            print(f"Title: {root_catalog.title or 'N/A'}")
            print(f"Description: {root_catalog.description or 'N/A'}")

            # Print STAC Items
            items = list(root_catalog.get_all_items())

            print(f"Number of items: {len(items)}")

            for item in items:
                item_id = item.id
                metadata = item.properties
                bbox = item.bbox
                footprint = item.geometry
                print(f"- {item.id}")
                print(f"  - {item.self_href}")
    except:
        traceback.print_exc()
        raise Exception("ERROR: Unable to read Catalog")


def parser():
    '''
    Construct a parser to parse arguments
    @return argparse parser
    '''
    parse = argparse.ArgumentParser(description="Outline details of STAC Catalog")
    parse.add_argument('catalog', nargs=1, type=str, help='Remote or local STAC catalog path (example: https://raw.githubusercontent.com/scottyhq/sentinel1-rtc-stac/main/19TCH/2021/catalog.json)')
    return parse


if __name__ == "__main__":
    main()
