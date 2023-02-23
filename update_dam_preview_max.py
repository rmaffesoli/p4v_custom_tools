from __future__ import print_function

import os
import random
import tempfile
import string
import binascii

import subprocess
from pymxs import runtime as mxs


def gen_max_thumbs():

    img_dict = {
        "thumb": "png",
        "preview": "png",
    }
    file_dir = mxs.maxFilePath
    file_name = mxs.maxFileName

    with tempfile.TemporaryDirectory() as tmp_dir:
        filepath = os.path.join(
            tmp_dir, "".join(random.sample(string.ascii_letters, 12))
        )
        img_path = ".".join([filepath, "jpg"])
        screen_shot = mxs.gw.getViewportDib()
        screen_shot.filename = img_path
        mxs.save(screen_shot)
        with open(img_path, "rb") as f:
            hex_string = binascii.hexlify(f.read())
            for attr in ["preview", "thumb", "blur"]:
                commands = ["p4", "attribute", "-fei", "-n", attr, file_name]

                if attr == "blur":
                    commands = ["p4", "attribute", "-fi", "-n", attr, file_name]
                    hex_string = bytes("U4DbZs009u=X7O9a599t=EtQ~U-U01~C0Mxa", "utf-8")
                p = subprocess.Popen(
                    commands,
                    stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=file_dir,
                )

                attr_stdout = p.communicate(input=hex_string)[0]
                print(attr_stdout.decode())


gen_max_thumbs()
