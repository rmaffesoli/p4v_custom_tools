#!/usr/bin/env python
from __future__ import print_function

import os
import argparse
import socket


def export_p4_config(ws_root, port, ws, user, ignore_filename):
    config_filename = ".p4config"
    config_filepath = os.path.join(ws_root, config_filename)
    lines = [
        "P4PORT={}\n".format(port),
        "P4CLIENT={}\n".format(ws),
        "P4USER={}\n".format(user),
        "P4HOST={}\n".format(socket.gethostname()),
        "P4IGNORE={}\n".format(ignore_filename),
    ]

    if os.path.exists(config_filepath):
        print(".p4config already exists")
        return

    with open(config_filepath, "w") as config_buffer:
        config_buffer.writelines(lines)
    print("p4config written to", config_filepath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ws_root")
    parser.add_argument("port")
    parser.add_argument("ws")
    parser.add_argument("user")
    parser.add_argument("ignore_filename", nargs="?", default=None, const=".p4ignore")

    parsed_args = parser.parse_args()

    export_p4_config(
        parsed_args.ws_root,
        parsed_args.port,
        parsed_args.ws,
        parsed_args.user,
        parsed_args.ignore_filename,
    )
