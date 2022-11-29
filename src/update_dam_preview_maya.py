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

    img_dict = {"thumb": "jpg", "preview": "png"}
    file_dir, file_name = os.path.split(cmds.file(sn=1, q=1))
    with tempfile.TemporaryDirectory() as tmp_dir:
        filepath = os.path.join(tmp_dir, get_random_word())
        for attribute, extension in img_dict.items():
            img_path = ".".join([filepath, extension])
            cmds.refresh(cv=True, fe=extension, fn=img_path)
            with open(img_path, "rb") as f:
                hex_string = binascii.hexlify(f.read())
                p = subprocess.Popen(
                    ["p4", "attribute", "-fei", "-n", attribute, file_name],
                    stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=file_dir,
                )
                attr_stdout = p.communicate(input=hex_string)[0]
                print(attr_stdout.decode())


def get_random_word(length=12):
    return "".join(random.sample(string.ascii_letters, length))


gen_maya_thumbs()
