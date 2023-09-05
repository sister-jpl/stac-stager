import os
import json
import rasterio
import urllib.request
import pystac
import traceback
import shutil
import argparse

from datetime import datetime, timezone
from shapely.geometry import Polygon, mapping
from tempfile import TemporaryDirectory
from urllib.request import urlretrieve
from pystac import Catalog, get_stac_version
from pystac.extensions.eo import EOExtension
from pystac.extensions.label import LabelExtension
from osaka.main import get


def main():
    # get args
    args = parser().parse_args()

    # create temp dir
    tmp_dir = "./{}".format(args.tag)
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)    
    os.mkdir(tmp_dir)

    # context = args.list
    context = get_properties(args.catalog, tmp_dir=tmp_dir)

    # create stac catalog
    tag = args.tag
    catalog = pystac.Catalog(id=tag, 
                            description='This catalog contains localized urls for {}'.format(tag))

    # add stac items
    if len(context) > 0:
        for product in context:
            datetime_utc = datetime.now(tz=timezone.utc)
            item = pystac.Item(id=product["item"],
                    geometry=product["footprint"],
                    bbox=product["bbox"],
                    datetime=datetime_utc,
                    properties=product["metadata"])
            item.add_asset(
                key='product',
                asset=pystac.Asset(
                    href="./{}".format(product["item"])
                )
            )
            catalog.add_item(item)

    # set catalog hrefs
    catalog.normalize_hrefs(tmp_dir)

    # save the catalog
    catalog.describe()
    catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)
    print("Catalog HREF: ", catalog.get_self_href())
    print("Item HREF: ", item.get_self_href())
    # tmp_dir.cleanup()


def get_properties(catalog, tmp_dir=False):
    """ Purpose: Get bbox, footprint, and metadata from Catalog items. """
    try:
        context = []

        # Read the example catalog
        root_catalog = Catalog.from_file(catalog)

        root_catalog.describe()

        # Print STAC Items
        items = list(root_catalog.get_all_items())

        for item in items:
            item_id = item.id
            metadata = item.properties
            bbox = item.bbox
            footprint = item.geometry
            filename = item.self_href.split("/")[-1]
            filename_path = "./{}".format(filename)
            get(item.self_href, filename)
            if tmp_dir:
                shutil.copy(filename_path, os.path.join(tmp_dir, filename))
            context.append({"item": item_id, "metadata": metadata, "bbox": bbox, "footprint": footprint})

        return context
    except:
        # tmp_dir.cleanup()
        traceback.print_exc()
        raise Exception("Unable to get properties for '{}'".format(catalog))


def parser():
    '''
    Construct a parser to parse arguments
    @return argparse parser
    '''
    parse = argparse.ArgumentParser(description="Create a local STAC catalog output based on remote STAC catalog input.")
    parse.add_argument('-c', '--catalog', help='File containing list of paths to products (Example: https://raw.githubusercontent.com/scottyhq/sentinel1-rtc-stac/main/19TCH/2021/catalog.json)', dest='catalog', required=True)
    parse.add_argument('-t', '--tag', help='Name/ID for STAC catalog [default: "local-stac"]', dest='tag', default="local-stac", required=False)
    return parse


if __name__ == "__main__":
    main()
