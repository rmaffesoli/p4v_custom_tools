from __future__ import print_function

import os
import random
import tempfile
import string
import binascii

import subprocess

# from maya import cmds
# import p4


def gen_maya_thumbs():
    file_dir, file_name = os.path.split(cmds.file(sn=1, q=1))
    with tempfile.TemporaryDirectory() as tmp_dir:
        filepath = os.path.join(tmp_dir, get_random_word())
        img_path = ".".join([filepath, "jpg"])
        cmds.refresh(cv=True, fe="jpg", fn=img_path)

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


def get_random_word(length=12):
    return "".join(random.sample(string.ascii_letters, length))


gen_maya_thumbs()
