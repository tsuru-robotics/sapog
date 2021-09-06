#!/usr/bin/python3
#  Copyright (c) 2021 Zubax, zubax.com
#  Distributed under the MIT License, available in the file LICENSE.
#  Author: Silver Valdvee <silver.valdvee@zubax.com>
import argparse
import os
from os import walk
from os import getcwd
import platform
import re
from pathlib import Path



def follow_link(link):
    print(f"The link is at: {str(link)}")
    actual_location = os.readlink(os.path.join(r"/dev/serial/by-id/", str(link)))
    print(f"{actual_location} is the actual location of the port found.")
    new_actual_location = actual_location
    try:
        while True:
            new_actual_location = os.readlink(actual_location)
            if new_actual_location == actual_location:
                break
            else:
                actual_location = new_actual_location
                print("A link hop was done.")
        print(f"{new_actual_location} was followed from links.")
    except FileNotFoundError:
        pass
    return actual_location


def get_port():
    if "Linux" in platform.uname().system:
        pattern = re.compile(r".*Black.*Magic.*Probe.*0$")
        files = next(walk(Path(r"/dev/serial/by-id/")), [(None, None, [])])[2]
    elif "Darwin" in platform.uname().system:
        # Converted from this PORT=$(ls /dev/cu.usb[sm][eo][rd][ie][am]* | head -n 1)
        pattern = re.compile(r"/dev/cu.usb[sm][eo][rd][ie][am]*")
        files = next(walk(Path(r"/dev/")), [(None, None, [])])[2]
    else:
        raise NotImplemented(f"Platform {platform.uname().system} not supported yet.")
    my_filter = lambda x: pattern.search(str(x))
    files = list(filter(my_filter, files))
    if len(files) > 1:
        print("There are too many ports to choose from:")
        for port in files:
            print(f"Port name: {port}")
    else:
        return follow_link(files[0])



def upload_file(port_file, elf_file, gdb_name, size_name):
    stream = os.popen(f"{size_name} {elf_file}") # arm-none-eabi-size $elf
    output = stream.read()


def get_needed_elf_file():
    files = next(walk(getcwd()), [(None, None, [])])[2]
    files = filter(lambda x: str(x).endswith(".elf"), files)
    enumerated_files = list(enumerate(files))
    print()
    if len(enumerated_files) > 1:
        print("No input files were specified, now looking for elf files, would like to use any of them?")
        for index, file in enumerated_files:
            print(f"nr {index}. file name: {file}")
        requested_nr = int(input("Enter the number of the file you would like to be uploaded: "))
        if len(enumerated_files) > requested_nr > -1:
            requested_file = enumerated_files[requested_nr][1]
            print(f"Requested file {requested_file} will be uploaded.")
    elif len(enumerated_files) == 1:
        print("No input files were specified.")
        print("Also, only one elf file is available.")
        answer = input(f"Use {enumerated_files[0][1]}? (Y/n)")
        if str.lower(answer) == "n":
            return None
        return enumerated_files[0]


def no_given_file_scenario():
    return get_needed_elf_file(), get_port()


def file_given_scenario(file):
    return file, get_port


def main():
    print(platform.uname())
    get_port()
    if "Linux" not in platform.uname().system:
        # TODO: The reference sh script had support for Darwin too
        raise Exception("Only linux distributions are supported")
    try:
        parser = argparse.ArgumentParser(description='Upload a new binary to the microcontroller through blackmagic.')
        parser.add_argument('input_file', help='an elf file to read in')
        parser.add_argument('-g', '--gdb-executable')
        args = parser.parse_args()
        print(args)
    except:
        try:
            no_given_file_scenario()
        except KeyboardInterrupt:
            print(os.linesep + 'Okay, good luck!')


if __name__ == '__main__':
    main()
