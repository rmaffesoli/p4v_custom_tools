#!/usr/bin/python 

####################################################################################################
# (c) Marwan Abdellah, Blue Brain Project, Ecole Polytechnique Federal de Lausanne (EPFL) 
####################################################################################################

# Imports 
import binascii
import os
import subprocess
import random
import string
import tempfile

from P4 import P4, P4Exception

p4 = P4()
p4.user = 'username'
p4.port = 'p4_port'
p4.connect()

def gen_exr_dam_preview_attr(depot_path):
    with tempfile.TemporaryDirectory() as temp_dir:
        filepath = os.path.join(temp_dir, get_random_word())
        img_path = ".".join([filepath, "png"])
    
        temp_exr = os.path.join(temp_dir,"temp.exr")
        p4.run("print", "-q", "-o", f"{temp_exr}", depot_path)

        
        conversion_args = '-gamma %s -channel ALL -normalize -quality 100' % (1.5)
        shell_command = 'magick convert %s %s %s ' % (temp_exr, conversion_args, img_path)
        print('CONVERTING: ' + shell_command)
        subprocess.call(shell_command, shell=True)

        with open(img_path, "rb") as file_buff:
            hex_string = binascii.hexlify(file_buff.read())
            p4.run(
                "attribute",
                "-fe",
                "-n",
                "preview",
                "-v",
                hex_string,
                f"{depot_path}",
                )
            print("Attributes set.")
    

def get_random_word(length=12):
    return "".join(random.sample(string.ascii_letters, length))

     
####################################################################################################
# @main
####################################################################################################
def main(changelist):
    description = p4.run_describe(changelist)
    for i, depot_file in enumerate(description[0]["depotFile"]):
        if depot_file.lower().endswith(".exr"):
            if 'delete' not in description[0]['action'][i]:
                gen_exr_dam_preview_attr(f"{depot_file}@{changelist}")


if __name__ == '__main__':
    main(2790)