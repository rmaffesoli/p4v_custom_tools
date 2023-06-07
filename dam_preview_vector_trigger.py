# -*- coding: utf-8 -*-
import os
import random
import tempfile
import string
import binascii
import argparse
import subprocess

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image

from pathlib import Path

from P4 import P4, P4Exception

P4PORT = "ssl:192.168.0.32:1666"
P4USER = "rmaffesoli"

p4 = P4()
p4.connect()


def gen_eps_dam_preview_attr(depot_path: str):
    with tempfile.TemporaryDirectory() as temp_dir:
        filepath = os.path.join(temp_dir, get_random_word())
        img_path = ".".join([filepath, "jpg"])

        temp_eps = Path(temp_dir) / "temp.eps"
        p4.run("print", "-q", "-o", f"{temp_eps}", depot_path)
        eps_image = Image.open(temp_eps)
        eps_image.load(scale=10)
        eps_image.save(img_path)

        with open(img_path, "rb") as file_buff:
            hex_string = binascii.hexlify(file_buff.read())
            for attr in ["thumb", "preview", "blur"]:
                args = '-fe'
                if attr == "blur":
                    args = '-f'
                    hex_string = bytes("U4DbZs009u=X7O9a599t=EtQ~U-U01~C0Mxa", "utf-8")

                p4.run(
                    "attribute",
                    f"{args}",
                    "-n",
                    f"{attr}",
                    "-v",
                    hex_string,
                    f"{depot_path}",
                )
            print("Attributes set.")


def gen_svg_dam_thumb_attr(depot_path: str):
    with tempfile.TemporaryDirectory() as temp_dir:
        filepath = os.path.join(temp_dir, get_random_word())
        img_path = ".".join([filepath, "jpg"])

        temp_svg = Path(temp_dir) / "temp.svg"
        p4.run("print", "-q", "-o", f"{temp_svg}", depot_path)

        drawing = svg2rlg(temp_svg)
        renderPM.drawToFile(drawing, img_path, fmt="JPG")

        with open(img_path, "rb") as file_buff:
            hex_string = binascii.hexlify(file_buff.read())
            for attr in ["thumb", "blur"]:
                args = '-fe'
                if attr == "blur":
                    args = '-f'
                    hex_string = bytes("U4DbZs009u=X7O9a599t=EtQ~U-U01~C0Mxa", "utf-8")

                p4.run(
                    "attribute",
                    f"{args}",
                    "-n",
                    f"{attr}",
                    "-v",
                    hex_string,
                    f"{depot_path}",
                )
            print("Attributes set.")


def get_random_word(length=12):
    return "".join(random.sample(string.ascii_letters, length))


def main(changelist):
    description = p4.run_describe(changelist)
    for file in description[0]["depotFile"]:
        if file.endswith(".svg"):
            gen_eps_dam_preview_attr(f"{file}@{changelist}")
        elif file.endswith(".eps"):
            gen_svg_dam_thumb_attr(f"{file}@{changelist}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("changelist")

    parsed_args = parser.parse_args()
    main(parsed_args.changelist)
