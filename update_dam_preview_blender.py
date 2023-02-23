from __future__ import print_function


import binascii
import bpy
import random
import os
import string
import sys
import subprocess
import tempfile


def gen_blender_thumbs():
    file_dir, file_name = os.path.split(bpy.data.filepath)
    with tempfile.TemporaryDirectory() as tmp_dir:
        filepath = os.path.join(tmp_dir, get_random_word())
        img_path = ".".join([filepath, "jpg"])
        generate_preview(img_path)

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


def generate_preview(img_path):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == "VIEW_3D":
                for space in area.spaces:
                    if space.type == "VIEW_3D":
                        for region in area.regions:
                            if region.type == "WINDOW":
                                L_altBpyCtx = {
                                    "area": area,
                                    "blend_data": bpy.context.blend_data,
                                    "region": None,
                                    "space": space,
                                    "window": window,
                                }
                                bpy.ops.screen.screenshot(
                                    L_altBpyCtx, filepath=img_path
                                )
                                break
                        break
                break


gen_blender_thumbs()
