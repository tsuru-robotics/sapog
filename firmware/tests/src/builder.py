#
# Copyright (c) 2021 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#
import argparse
import asyncio
import pathlib
import sys

source_path = pathlib.Path(__file__).parent.absolute()
dependency_path = source_path.parent / "deps"
namespace_path = dependency_path / "namespaces"
sys.path.insert(0, namespace_path.absolute())

from multiprocessing import cpu_count
import subprocess
import requests

downloads_folder_name = "downloads"
tracking_branch_name = "v3"
assert (len(downloads_folder_name) > 4)
downloads_folder_name = downloads_folder_name.replace("*", "")
remove_zip_files_after_use = True
sapog_root = pathlib.Path(__file__).parent.parent.parent.parent.absolute()
firmware_directory = sapog_root / "firmware"
tests_directory = firmware_directory / "tests"


def get_port():
    from glob import glob
    output = subprocess.check_output(
        ["realpath", "-LPz", glob("/dev/serial/by-id/usb-*Black_Magic_Probe*-if00")[0]]).decode("utf-8")[:-1]
    return output


def move_directories(destination: pathlib.Path, *source_dirs: pathlib.Path):
    subprocess.run(["mv", "-ut", destination, *source_dirs])


async def upload_sapog():
    temp_file = f"""tar ext {get_port()}
mon swdp_scan
attach 1
set mem inaccessible-by-default off
load
quit"""
    arguments = []
    for line in temp_file.split("\n"):
        arguments.append("-ex")
        arguments.append(f"{line.rstrip()}")  # https://manned.org/arm-none-eabi-gdb/7308522e
    subprocess.run(
        ["/home/zubaxpc/gcc-arm-none-eabi-10.3-2021.10/bin/arm-none-eabi-gdb",
         firmware_directory / "build" / "compound.elf", *arguments,
         "--batch"], shell=True, check=True)


async def build_sapog() -> None:
    public_regulated_data_types_directory = (firmware_directory / "public_regulated_data_types").absolute()
    subprocess.run(["make", "clean"], cwd=firmware_directory)
    subprocess.run(["mkdir", firmware_directory / downloads_folder_name])
    import zipfile
    # making a request for downloading the zip file
    url = "https://github.com/UAVCAN/public_regulated_data_types/archive/refs/heads/master.zip"
    r = requests.get(url, allow_redirects=True)
    # writing the received binary to a file
    zip_path = firmware_directory / downloads_folder_name / "public_regulated_data_types.zip"
    public_regulated_data_types = open(zip_path, "wb")
    public_regulated_data_types.write(r.content)
    public_regulated_data_types.close()
    zip_file = zipfile.ZipFile(zip_path)
    name_list = zip_file.namelist()
    extra_parent_directory = name_list[0]
    zip_file.extractall(firmware_directory / downloads_folder_name)
    zip_file.close()
    subprocess.run(["mkdir", public_regulated_data_types_directory])
    print("Created the directory for public_regulated_data_types")
    move_directories(public_regulated_data_types_directory,
                     (firmware_directory / downloads_folder_name / extra_parent_directory / "uavcan").absolute(),
                     (firmware_directory / downloads_folder_name / extra_parent_directory / "reg").absolute())


async def start_build_process() -> None:
    await build_sapog()


async def main() -> None:
    await build_sapog()


already_ran = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "A script that builds Sapog or uploads the built elf file to the device through"
        "Blackmagic based Babel-Babel.")
    parser.add_argument("action", choices=["build", "flash"], nargs="?")
    args = parser.parse_args()
    if args.action == "build":
        asyncio.get_event_loop().run_until_complete(build_sapog())
    elif args.action == "flash":
        asyncio.get_event_loop().run_until_complete(upload_sapog())
    else:
        parser.print_help()
        exit(1)
