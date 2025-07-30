#!/usr/bin/env python
from __future__ import print_function

import os
import binascii

import subprocess
import argparse


def attach_glb_preview_attr(selected_asset, thumb_path, glb_path):
    file_dir, file_name = os.path.split(selected_asset)

    attr_path_dict = {
        'thumb': thumb_path,
        'preview': thumb_path,
        'model': glb_path, 
    }

    for attr, file_path in attr_path_dict.items():
        commands = ["p4", "attribute", "-f", "-I", file_path, "-n", attr, file_name]
        proc = subprocess.Popen(
            commands,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=file_dir,
        )

        attr_stdout = proc.communicate()[0]
        print(attr_stdout.decode())


    simple_attr_dict = {
        "blur": "U4DbZs009u=X7O9a599t=EtQ~U-U01~C0Mxa",
        "blur_size": "240x180",
    }

    for attr, value_str in simple_attr_dict.items():
        commands = ["p4", "attribute", "-fi", "-n", attr, file_name]
        byte_string = bytes(value_str, "utf-8")
        proc = subprocess.Popen(
            commands,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=file_dir,
        )

        attr_stdout = proc.communicate(input=byte_string)[0]
        print(attr_stdout.decode())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("selected_asset")
    parser.add_argument("thumbnail_file")
    parser.add_argument("glb_file")

    parsed_args = parser.parse_args()

    attach_glb_preview_attr(parsed_args.selected_asset, parsed_args.thumbnail_file, parsed_args.glb_file)
