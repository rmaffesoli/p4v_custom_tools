#!/usr/bin/env python
from __future__ import print_function

import os
import binascii

import subprocess
import argparse


def attach_preview_attr(selected_asset, img_path):
    file_dir, file_name = os.path.split(selected_asset)
    with open(img_path, "rb") as file_buff:
        hex_string = binascii.hexlify(file_buff.read())

        for attr in ["preview", "thumb", "blur"]:
            commands = ["p4", "attribute", "-fei", "-n", attr, file_name]

            if attr == "blur":
                commands = ["p4", "attribute", "-fi", "-n", attr, file_name]
                hex_string = bytes("U4DbZs009u=X7O9a599t=EtQ~U-U01~C0Mxa", "utf-8")
            proc = subprocess.Popen(
                commands,
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=file_dir,
            )

            attr_stdout = proc.communicate(input=hex_string)[0]
            print(attr_stdout.decode())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("selected_asset")
    parser.add_argument("image_file")

    parsed_args = parser.parse_args()

    attach_preview_attr(parsed_args.selected_asset, parsed_args.image_file)
