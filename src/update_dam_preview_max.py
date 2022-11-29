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
        'thumb': 'png',
        'preview': 'png',
    }
    file_dir = mxs.maxFilePath
    file_name  = mxs.maxFileName

    with tempfile.TemporaryDirectory() as tmp_dir:
        filepath = os.path.join(
            tmp_dir, 
            "".join(random.sample(string.ascii_letters, 12))
        )
        for attribute, extension in img_dict.items():
            img_path = '.'.join([filepath, extension])
            screen_shot=mxs.gw.getViewportDib()
            screen_shot.filename = img_path
            mxs.save(screen_shot)
            with open(img_path, 'rb') as f:
                hex_string = binascii.hexlify(f.read())
                print(attribute, hex_string)
                p = subprocess.Popen(
                    ['p4', 'attribute', '-fei', '-n', attribute, file_name], 
                    stdout=subprocess.PIPE, 
                    stdin=subprocess.PIPE, 
                    stderr=subprocess.STDOUT,
                    cwd=file_dir
                )    
                attr_stdout = p.communicate(input=hex_string)[0]
                print(attr_stdout.decode())


gen_max_thumbs()
