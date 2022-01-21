#!/bin/bash
# Copyright (c) 2015 Zubax Robotics, zubax.com
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>

function die()
{
    echo "$@" 1>&2
    exit 1
}

[[ $EUID -ne 0 ]] || die "Do NOT run this script as root.
If you resorted to root because the debugger cannot be accessed by a regular user, \
follow this guide to configure the access permissions correctly: https://kb.zubax.com/x/N4Ah"

PORT="$1"
if [ -z "$PORT" ]
then
    if [ "$(uname)" == "Darwin" ]
    then
        PORT=$(ls /dev/cu.usb[sm][eo][rd][ie][am]* | head -n 1)
    else
        PORT=$(readlink -f /dev/serial/by-id/*Black*Magic*Probe*0)
    fi

    [ -e "$PORT" ] || die "Debugger not found"
    echo "Using port $PORT"
fi

elf=build/bootloader.elf
[ -e "$elf" ] || die "ELF file could not be found"

arm-none-eabi-size $elf || die "Could not check the size of the binary"

temp_file=.blackmagic_gdb.tmp
cat > $temp_file <<EOF
target extended-remote $PORT
mon swdp_scan
attach 1
load
kill
EOF

# Key -n to ignore .gdbinit
arm-none-eabi-gdb $elf -n --batch -x $temp_file

rm -f $temp_file
