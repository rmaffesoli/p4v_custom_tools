# -*- coding: utf-8 -*-
import os
import random
import tempfile
import string
import binascii
import argparse
import subprocess

from PIL import Image


def gen_dds_dam_preview_attr(dds_filepath):
    file_dir, file_name = os.path.split(dds_filepath)

    with tempfile.TemporaryDirectory() as tmp_dir:
        filepath = os.path.join(tmp_dir, get_random_word())
        img_path = ".".join([filepath, "png"])
       

        dds_image = Image.open(dds_filepath)
        dds_image.load()
        dds_image.save(img_path)

        with open(img_path, "rb") as file_buff:
            hex_string = binascii.hexlify(file_buff.read())
            commands = ["p4", "attribute", "-fei", "-n", "preview", file_name]

            proc = subprocess.Popen(
                commands,
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=file_dir,
            )

            attr_stdout = proc.communicate(input=hex_string)[0]
            print(attr_stdout.decode())


def get_random_word(length=12):
    return "".join(random.sample(string.ascii_letters, length))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dds_filepath")

    parsed_args = parser.parse_args()
    gen_dds_dam_preview_attr(parsed_args.dds_filepath)
