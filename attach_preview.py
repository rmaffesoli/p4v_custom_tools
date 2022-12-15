#!/usr/bin/env python
from __future__ import print_function

import os
import random
import tempfile
import string
import binascii

import subprocess
import argparse


def attach_preview_attr(selected_asset, img_path):
    file_dir, file_name = os.path.split(selected_asset)
    with open(img_path, "rb") as f:
        hex_string = binascii.hexlify(f.read())
        for attr in ["preview", "thumb"]:
            p = subprocess.Popen(
                ["p4", "attribute", "-ei", "-n", attr, file_name],
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=file_dir,
            )
            attr_stdout = p.communicate(input=hex_string)[0]
            print(attr_stdout.decode())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("selected_asset")
    parser.add_argument("image_file")

    parsed_args = parser.parse_args()

    attach_preview_attr(parsed_args.selected_asset, parsed_args.image_file)
