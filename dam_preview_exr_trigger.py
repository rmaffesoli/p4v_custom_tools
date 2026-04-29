#!/usr/bin/python

import binascii
import os
import subprocess
import random
import logging
import string
import tempfile
import argparse
from wand.image import Image

from P4 import P4, P4Exception

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
fh = logging.FileHandler('/home/perforce/triggers/create_exr_thumbnails/create_exr_thumbnails.log')
logger.addHandler(fh)

p4 = P4()
p4.user = 'username'
p4.port = 'p4port'
p4.connect()

def gen_exr_dam_preview_attr(depot_path):
    with tempfile.TemporaryDirectory() as temp_dir:
        filepath = os.path.join(temp_dir, get_random_word())
        img_path = ".".join([filepath, "png"])

        temp_exr = os.path.join(temp_dir,"temp.exr")
        p4.run("print", "-q", "-o", f"{temp_exr}", depot_path)

        with Image(filename=temp_exr) as img:
            img.colorspace = 'rgb'
            img.transform_colorspace('srgb')
            img.format = 'png'
            img.save(filename=img_path)

        logger.info('CONVERSION DONE')
        logger.info('img_path: %s, exists: %s', img_path, os.path.exists(img_path))
        logger.info('temp_exr: %s, exists: %s', temp_exr, os.path.exists(temp_exr))

        with open(img_path, "rb") as file_buff:
            hex_string = binascii.hexlify(file_buff.read())
            p4.run(
                "attribute",
                "-fe",
                "-n",
                "preview",
                "-v",
                hex_string,
                f"{depot_path}",
                )
            logger.info("Attributes set.")


def get_random_word(length=12):
    return "".join(random.sample(string.ascii_letters, length))


def main(changelist):
    description = p4.run_describe(changelist)
    for i, depot_file in enumerate(description[0]["depotFile"]):
        if depot_file.lower().endswith(".exr"):
            if 'delete' not in description[0]['action'][i]:
                gen_exr_dam_preview_attr(f"{depot_file}@{changelist}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("changelist")

    parsed_args = parser.parse_args()
    main(parsed_args.changelist)