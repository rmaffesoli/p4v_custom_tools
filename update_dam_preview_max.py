from __future__ import print_function

import os
import random
import tempfile
import string
import binascii

import subprocess
from pymxs import runtime as mxs


def genMaxThumbs():
    img_dict = {
        "thumb": "png",
        "preview": "png",
    }
    file_dir = mxs.maxFilePath
    file_name = mxs.maxFileName

    if not (file_dir and file_name):
        print("No valid File Path")
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
                commands = ["p4", "attribute", "-fei", "-n", attr, -v, hex_string, file_name]

                if attr == "blur":
                    commands = ["p4", "attribute", "-fi", "-n", attr, -v, hex_string, file_name]
                    hex_string = bytes("U4DbZs009u=X7O9a599t=EtQ~U-U01~C0Mxa", "utf-8")
                p = subprocess.Popen(
                    commands,
                    stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=file_dir,
                )

                #~ attr_stdout = p.communicate(input=hex_string)[0]
                #~ print(attr_stdout.decode())


def menu_callback():
    menu = mxs.callbacks.notificationparam()
    main_menu = menu.mainmenubar


    sub_menu = main_menu.createsubmenu("88e2fb4c-1111-1a2a-a1aa-7cc61cbb0358", "p4tools")
        
    macro_id = 647394 
    sub_menu.createaction("88e2fb4c-1111-1a2a-a2aa-7cc61cbb0358", macro_id, "genMaxThumbsAction`p4tools")


mxs.macros.new(
    'p4tools',
    'genMaxThumbsAction',
    'Generate P4Dam Preview',
    "Generate P4Dam Preview",
    "genMaxThumbs()"
)

mxs.genMaxThumbs = genMaxThumbs
menu_script = mxs.name("p4tools")
mxs.callbacks.removescripts(id=menu_script)
mxs.callbacks.addscript(mxs.name("cuiRegisterMenus"), menu_callback, id=menu_script)

mxs.maxOps.GetICuiMenuMgr().LoadConfiguration(mxs.maxOps.GetICuiMenuMgr().getCurrentConfiguration())