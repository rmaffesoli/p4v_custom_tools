#!/usr/bin/env python
from __future__ import print_function

import os

import argparse
import socket
import subprocess

default_ue_p4ignore = [
    "Saved/",
    "LocalBuilds/",
    "*.csproj.*",
    ".vs/*",
    "*.pdb",
    "*.suo",
    "*.opensdf",
    "*.sdf",
    "*.tmp",
    "*.mdb",
    "obj/",
    "*.vcxproj",
    "*.sln",
    "*-Debug.*",
    "FileOpenOrder/",
    "*.xcworkspace",
    "*.xcodeproj",
    "./Makefile",
    "./CMakeLists.txt",
    ".ue4dependencies",
    "Samples/*",
    "FeaturePacks/*",
    "Templates/*",
    "Engine/Documentation/*",
    "\n# Engine intermediates",
    "Engine/Intermediate/*",
    "Intermediate/",
    "\n# Intermediate folders for programs should not be checked in",
    r"Engine\Programs\*\Intermediate\*",
    "\n# Intermediate folders created for various C# programs",
    r"Engine\Source\Programs\*\obj\*",
    "\n# Saved folders for programs should not be checked in",
    r"Engine\Programs\*\Saved\*",
    r"Engine\Programs\UnrealBuildTool\*",
    "\n# Derived data cache should never be checked in",
    "Engine/DerivedDataCache/*",
    "\n# Ignore any build receipts",
    "Engine/Build/Receipts/*",
    "\n# Ignore personal workspace vars",
    ".p4config",
    "\n# Ignore Unix backup files",
    "*~",
    "\n# Ignore Mac desktop services store files",
    ".DS_Store",
    "\n# Ignore crash reports",
    "crashinfo--*",
    "\n# Ignore linux project files",
    "*.user",
    "*.pro",
    "*.pri",
    "*.kdev4",
    "\n# Obj-C/Swift specific",
    "*.hmap",
    "*.ipa",
    "*.dSYM.zip",
    "*.dSYM",
    "\n# Ignore documentation generated for C# tools",
    "Engine/Binaries/DotNET/UnrealBuildTool.xml",
    "Engine/Binaries/DotNET/AutomationScripts/BuildGraph.Automation.xml",
    "\n# Ignore version files in the Engine/Binaries directory created by UBT",
    "/Engine/Binaries/**/*.version",
    "\n# Ignore exp files in the the Engine/Binaries directory as they aren't C/C++ source files",
    "/Engine/Binaries/**/*.exp",
    "\n# Ignore Swarm local save files",
    "Engine/Binaries/DotNET/SwarmAgent.DeveloperOptions.xml",
    "Engine/Binaries/DotNET/SwarmAgent.Options.xml",
    "\n# Intermediary Files",
    "*.target.xml",
    "*.exe.config",
    "*.exe.manifest",
    "\n# Ignore project-specific files",
    "GAMEPROJECT/Build/Receipts/*",
    "GAMEPROJECT/DerivedDataCache/*",
    "GAMEPROJECT/Binaries/*-Shipping.*",
    "GAMEPROJECT/Intermediate/*",
]

default_ue_typemap = [
    "# Perforce File Type Mapping Specifications.",
    "#",
    "#  TypeMap:     a list of filetype mappings; one per line.",
    "#               Each line has two elements:",
    "#",
    "#               Filetype: The filetype to use on 'p4 add'.",
    "#",
    "#               Path:     File pattern which will use this filetype.",
    "#",
    "# See 'p4 help typemap' for more information.",
    "",
    "TypeMap:",
    "        binary+S2w //depot/....exe",
    "        binary+S2w //depot/....dll",
    "        binary+S2w //depot/....lib",
    "        binary+S2w //depot/....app",
    "        binary+S2w //depot/....dylib",
    "        binary+S2w //depot/....stub",
    "        binary+S2w //depot/....ipa",
    "        binary //depot/....bmp",
    "        binary //depot/....png",
    "        binary //depot/....tga",
    "        binary //depot/....raw",
    "        binary //depot/....r16",
    "        binary //depot/....mb",
    "        binary //depot/....fbx",
    "        text //depot/....ini",
    "        text //depot/....config",
    "        text //depot/....cpp",
    "        text //depot/....h",
    "        text //depot/....c",
    "        text //depot/....cs",
    "        text //depot/....m",
    "        text //depot/....mm",
    "        text //depot/....py",
    "        binary+l //depot/....uasset",
    "        binary+l //depot/....umap",
    "        binary+l //depot/....upk",
    "        binary+l //depot/....udk",
]


def export_p4_config(ws_root, port, ws, user):
    config_filename = ".p4config"
    ignore_filename = ".p4ignore"
    config_filepath = os.path.join(ws_root, config_filename)
    lines = [
        "P4PORT={}\n".format(port),
        "P4CLIENT={}\n".format(ws),
        "P4USER={}\n".format(user),
        "P4HOST={}\n".format(socket.gethostname()),
        "P4IGNORE={}\n".format(ignore_filename),
    ]

    if os.path.exists(config_filepath):
        os.remove(config_filepath)

    with open(config_filepath, "w") as config_buffer:
        config_buffer.writelines(lines)
    print("p4config written to", config_filepath)


def export_p4_ignore(ws_root, ue_project_name):
    ignore_filename = ".p4ignore"
    ignore_filepath = os.path.join(ws_root, ignore_filename)
    lines = [
        _.replace("GAMEPROJECT", ue_project_name) + "\n" for _ in default_ue_p4ignore
    ]

    if os.path.exists(ignore_filepath):
        os.remove(ignore_filepath)

    with open(ignore_filepath, "w") as ignore_buffer:
        ignore_buffer.writelines(lines)

    print("p4ignore written to", ignore_filepath)


def get_stream_name(ws_root):
    p = subprocess.Popen(
        ["p4", "-F", '"%Stream%"', "-ztag", "client", "-o"],
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=ws_root,
    )

    stream_stdout = p.communicate()[0]
    stream = stream_stdout.decode().replace("\r\n", "").replace('"', "")

    return stream


def setup_p4_typemap(ws_root):
    stream_name = get_stream_name(ws_root)
    depot_name = [_ for _ in stream_name.split("/") if _][0]
    typemap_string = "\n".join(
        [_.replace("depot", depot_name) for _ in default_ue_typemap]
    )
    p = subprocess.Popen(
        ["p4", "typemap", "-i"],
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=ws_root,
    )
    typemap_stdout = p.communicate(input=typemap_string.encode("utf-8"))[0]
    print(typemap_stdout.decode())


def setup_for_unreal(ws_root, port, ws, user, ue_project_name):
    export_p4_config(ws_root, port, ws, user)
    export_p4_ignore(ws_root, ue_project_name)
    setup_p4_typemap(ws_root)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ws_root")
    parser.add_argument("port")
    parser.add_argument("ws")
    parser.add_argument("user")
    parser.add_argument("ue_project_name")

    parsed_args = parser.parse_args()

    setup_for_unreal(
        parsed_args.ws_root,
        parsed_args.port,
        parsed_args.ws,
        parsed_args.user,
        parsed_args.ue_project_name,
    )
