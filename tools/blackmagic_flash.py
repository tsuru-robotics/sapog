#!/usr/bin/python3
#  Copyright (c) 2021 Zubax, zubax.com
#  Distributed under the MIT License, available in the file LICENSE.
#  Author: Silver Valdvee <silver.valdvee@zubax.com>
import argparse
import os
from os import walk
import platform
import re
from pathlib import Path
import builtins as __builtin__

verbose = False
doDump = False
dumpPath = ""

tempFile = """target extended-remote $PORT
mon swdp_scan
attach 1
load
kill
quit"""

tempFileDump = """target extended-remote $PORT
mon swdp_scan
attach 1
load
dump bin mem $PATH_DUMP 0x08000000 0x08040000
kill
quit"""


def say(*args, **kwargs):
    __builtin__.print(*args, **kwargs)


def print(*args, **kwargs):
    if verbose:
        __builtin__.print(*args, **kwargs)


def yes_or_no(message):
    answer = input(f"{message} (Y/n)")
    if str.lower(answer) == "n":
        return False
    return True


def follow_link(link):
    print(f"The link is at: {str(link)}")
    actual_location = os.readlink(str(link))
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
    print(f"Now {link} {actual_location}")
    return os.path.normpath(os.path.join(os.path.dirname(link), actual_location))


def get_port():
    if "Linux" in platform.uname().system:
        pattern = re.compile(r".*Black.*Magic.*Probe.*0$")
        chosenPath = r"/dev/serial/by-id/"
        files = next(walk(Path(chosenPath)), [(None, None, [])])[2]
    elif "Darwin" in platform.uname().system:
        pattern = re.compile(r"/dev/cu.usb[sm][eo][rd][ie][am]*")
        chosenpath = r"/dev/"
        files = next(walk(Path(chosenpath)), [(None, None, [])])[2]
    else:
        raise NotImplemented(f"Platform {platform.uname().system} not supported yet.")
    my_filter = lambda x: pattern.search(str(x))
    files = list(filter(my_filter, files))
    if len(files) > 1:
        say("There are too many ports to choose from:")
        for port in files:
            print(f"Port name: {port}")
    else:
        return follow_link(os.path.join(chosenPath, str(files[0])))


def upload_file(port_file, elf_file, gdb_name, size_name):
    stream = os.popen(f"{size_name} {elf_file}")  # arm-none-eabi-size $elf
    output = stream.read()
    if doDump:
        if len(dumpPath):
            tempFile2 = tempFileDump.replace("$PORT", port_file).replace("$PATH_DUMP", dumpPath)
        else:
            print("You did not specify a dumpPath.")
    else:
        tempFile2 = tempFile.replace("$PORT", port_file)
    arguments = []
    for line in tempFile2.split("\n"):
        arguments.append(f"-ex \"{line.rstrip()}\"")  # https://manned.org/arm-none-eabi-gdb/7308522e

    argument_string = " ".join(arguments)
    upload_command = f"{gdb_name} {elf_file} {argument_string} --batch"
    if yes_or_no(f"Should the upload command be run: {upload_command}"):
        stream = os.popen(upload_command)  # arm-none-eabi-size $elf
        output = stream.read()
        print(output)
    else:
        print("You didn't want to execute the command")
        exit(1)


def get_needed_elf_file(directory):
    files = next(walk(Path(directory)), (None, None, []))
    files = files[2]
    files = filter(lambda x: str(x).endswith(".elf"), files)
    enumerated_files = list(enumerate(files))
    say()
    if len(enumerated_files) > 1:
        print("No input files were specified, now looking for elf files, would like to use any of them?")
        for index, file in enumerated_files:
            print(f"nr {index}. file name: {file}")
        requested_nr = int(input("Enter the number of the file you would like to be uploaded: "))
        if len(enumerated_files) > requested_nr > -1:
            requested_file = enumerated_files[requested_nr][1]
            say(f"Requested file {requested_file} will be uploaded.")
            return requested_file
    elif len(enumerated_files) == 1:
        say("No input files were specified.")
        say("Also, only one elf file is available.")
        if not yes_or_no(f"Use {enumerated_files[0][1]}?"):
            say("You didn't select an elf file.")
            exit(1)
        else:
            return enumerated_files[0][1]
    else:
        if directory == os.getcwd():
            say("There are no elf files in the current working directory.")
        else:
            say(f"There are no elf files in: {directory}")
        exit(1)


def no_given_file_scenario(directory):
    return get_needed_elf_file(directory), get_port()


def file_given_scenario(file):
    return file, get_port()


def main():
    global verbose, doDump, dumpPath
    say("A flashing utility for Sapog.")
    print(platform.uname())
    get_port()
    if "Linux" not in platform.uname().system:
        # TODO: The reference sh script had support for Darwin too
        raise Exception("Only linux distributions are supported")
    try:
        parser = argparse.ArgumentParser(description='Upload a new binary to the microcontroller through blackmagic.')
        parser.add_argument('dir', nargs='?', default=os.getcwd(),
                            help="Searching for the elf file in this directory."
                                 " Defaults to the current working directory.")
        parser.add_argument('-i', '--input_file', help='an elf file to read in')
        parser.add_argument('-g', '--gdb-executable', default="arm-none-eabi-gdb")
        parser.add_argument('-s', '--size-executable', default="arm-none-eabi-size")
        parser.add_argument('-v', '--verbose', default=False, action='store_true')
        parser.add_argument('-d', '--dump', default=False, action='store_true')
        parser.add_argument('--dump-path', default=os.path.join(os.path.expanduser('~'), "magicdump.bin"))
        args = parser.parse_args()
        is_absolute = os.path.isabs(args.dir)
        if args.dir != os.getcwd() and not is_absolute:
            args.dir = os.path.join(os.getcwd(), args.dir)

        verbose = args.verbose
        doDump = args.dump
        dumpPath = args.dump_path
        if args.input_file:
            file, port = file_given_scenario(args.input_file)
        else:
            file, port = no_given_file_scenario(args.dir)
            file = os.path.join(args.dir, file)
        if not Path(file).exists():
            print("Your specified file doesn't exist.")
            exit(1)
        print(args)
        upload_file(port, file, args.gdb_executable, args.size_executable)
    except KeyboardInterrupt:
        print(os.linesep + 'Okay, good luck!')


if __name__ == '__main__':
    main()
