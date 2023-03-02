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


def gen_vector_dam_preview(vector_filepath):
    if vector_filepath.lower().endswith("eps"):
        gen_eps_dam_preview_attr(vector_filepath)
    elif vector_filepath.lower().endswith("svg"):
        gen_svg_dam_thumb_attr(vector_filepath)
    else:
        print("format unsupported at this time")


def gen_eps_dam_preview_attr(eps_filepath):
    file_dir, file_name = os.path.split(eps_filepath)

    with tempfile.TemporaryDirectory() as tmp_dir:
        filepath = os.path.join(tmp_dir, get_random_word())
        img_path = ".".join([filepath, "jpg"])

        eps_image = Image.open(eps_filepath)
        eps_image.load(scale=10)
        eps_image.save(img_path)

        with open(img_path, "rb") as file_buff:
            hex_string = binascii.hexlify(file_buff.read())
            for attr in ["thumb", "preview", "blur"]:
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


def gen_svg_dam_thumb_attr(svg_filepath):
    file_dir, file_name = os.path.split(svg_filepath)

    with tempfile.TemporaryDirectory() as tmp_dir:
        filepath = os.path.join(tmp_dir, get_random_word())
        img_path = ".".join([filepath, "jpg"])

        drawing = svg2rlg(svg_filepath)
        renderPM.drawToFile(drawing, img_path, fmt="JPG")

        with open(img_path, "rb") as file_buff:
            hex_string = binascii.hexlify(file_buff.read())
            for attr in ["thumb", "blur"]:
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


def get_random_word(length=12):
    return "".join(random.sample(string.ascii_letters, length))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("vector_filepath")

    parsed_args = parser.parse_args()
    gen_vector_dam_preview(parsed_args.vector_filepath)
