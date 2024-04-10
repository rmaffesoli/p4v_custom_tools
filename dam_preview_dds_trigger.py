# -*- coding: utf-8 -*-
import os
import sys
import random
import tempfile
import string
import binascii
import argparse

from PIL import Image

from pathlib import Path

from P4 import P4, P4Exception


p4 = P4()
p4.user = 'rmaffesoli'
p4.port = 'ssl:helix:1666'
p4.connect()


def gen_dds_dam_preview_attr(depot_path: str):
    with tempfile.TemporaryDirectory() as temp_dir:
        filepath = os.path.join(temp_dir, get_random_word())
        img_path = ".".join([filepath, "png"])

        temp_dds = os.path.join(temp_dir,"temp.dds")
        p4.run("print", "-q", "-o", f"{temp_dds}", depot_path)
        dds_image = Image.open(temp_dds)
        dds_image.load()
        dds_image.save(img_path)

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
            print("Attributes set.")


def get_random_word(length=12):
    return "".join(random.sample(string.ascii_letters, length))


def main(changelist):
    description = p4.run_describe(changelist)
    for depot_file in description[0]["depotFile"]:
        if depot_file.lower().endswith(".dds"):
            gen_dds_dam_preview_attr(f"{depot_file}@{changelist}")