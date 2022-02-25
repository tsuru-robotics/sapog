#
#   Copyright (C) 2013-2016 PX4 Development Team. All rights reserved.
#   Author: Pavel Kirienko <pavel.kirienko@gmail.com>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name PX4 nor the names of its contributors may be
#    used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# Edited by Silver Valdvee

PROJECT = io.px4.sapog

HW_VERSION_MAJOR = 1
FW_VERSION_MAJOR = 3
FW_VERSION_MINOR = 0

export SAPOG_BASE := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))
export SAPOG_SRC_DIR = $(abspath $(SAPOG_BASE)/src)

PYTHON := python3.8

#
# Sources
#

# https://stackoverflow.com/a/18258352
rwildcard=$(foreach d,$(wildcard $(1:=/*)),$(call rwildcard,$d,$2) $(filter $(subst *,%,$2),$d))

CSRC = $(call rwildcard,$(SAPOG_SRC_DIR),*.c) \
       $(wildcard $(SAPOG_SRC_DIR)/../include/*/*.c) \

CPPSRC = $(call rwildcard,$(SAPOG_SRC_DIR),*.cpp) \
         $(wildcard $(SAPOG_SRC_DIR)/../include/*/*.cpp)

UINCDIR = src           \
          src/os_config \
          generated/nunavut_out\
          "include" \

UDEFS = -DFW_VERSION_MAJOR=$(FW_VERSION_MAJOR)           \
        -DFW_VERSION_MINOR=$(FW_VERSION_MINOR)           \
        -DHW_VERSION_MAJOR=$(HW_VERSION_MAJOR)           \
        -DNODE_NAME=\"$(PROJECT)\"

# MAVLink v1 compliance
UDEFS += -DCONFIG_PARAM_MAX_NAME_LENGTH=92

#
# Git commit hash
#

GIT_HASH := $(shell git rev-parse --short HEAD)
DDEFS += -DBUILD_TIMESTAMP_UTC=$(shell date --utc +%s)
UDEFS += -DGIT_HASH=0x$(GIT_HASH)
UDEFS += -DVCS_REVISION_ID=0x$(shell git rev-parse --short=16 HEAD)

ifeq ($(git diff) $(git status -s), "")
    DDEFS += -DDIRTY_BUILD=0
else
    DDEFS += -DDIRTY_BUILD=1
endif
#
# OS
#

BUILD_CONFIG = 1
BUILD_CHIBIOS_SHELL = 1

SERIAL_CLI_PORT_NUMBER = 1

BOOTLOADER_SIZE = 59392 # Including 256 bytes for DeviceSignatureStorage


# This firmware is compatible with all versions of hardware where the major number is 1 (i.e. 1.x),
# therefore, the minor version is not specified here.
FW_VERSION_MAJOR_MINOR_VCS_HASH := $(FW_VERSION_MAJOR).$(FW_VERSION_MINOR).$(GIT_HASH)

DDEFS += -DCORTEX_VTOR_INIT=$(BOOTLOADER_SIZE)            \
         -DCRT1_AREAS_NUMBER=0                            \
         -DCONFIG_PARAMS_MAX=50	                          \
         -DBXCAN_MAX_IFACE_INDEX=1                        \
         -DBXCAN_BUSYWAIT_DELAY_SYSTEM_CORE_CLOCK=72000000

COMMON_SETTINGS_INCLUDED_BOOTLOADER_LINKER_FILE_PATH=$(SAPOG_SRC_DIR)/../../bootloader/linker.tmp.ld

COMMON_SETTINGS_INCLUDED_LINKER_FILE_PATH=$(SAPOG_SRC_DIR)/../linker.tmp.ld

LDSCRIPT=$(COMMON_SETTINGS_INCLUDED_LINKER_FILE_PATH)

USE_LTO = no
# Warning: GCC 4.9 with O3 and LTO breaks the code mysteriously! GCC 5.x segfaults during linking. Why GCC, why!?
RELEASE_OPT = -O3 -fomit-frame-pointer -DNDEBUG=1 -D"CANARD_ASSERT(x)" -fno-strict-aliasing
DEBUG_OPT = -Og -g3 -DDISABLE_WATCHDOG=1 -fno-strict-aliasing #-DNDEBUG=1 -D"CANARD_ASSERT(x)" -D"O1HEAP_ASSERT(x)"
# More warnings are enabled in the included makefile
CWARN = -Wshadow -Wpointer-arith -Wno-packed -Wno-attributes -Wno-error=undef -Wno-error=shadow #-Werror
CWARN += -Wno-error=implicit-fallthrough -Wno-deprecated
CPPWARN = $(CWARN)


COMPOUND_IMAGE_FILE := $(PROJECT)-$(HW_VERSION_MAJOR)-$(FW_VERSION_MAJOR_MINOR_VCS_HASH).compound.bin
BOOTLOADER_DIR := $(abspath $(SAPOG_BASE)/../bootloader)
BOOTLOADER_IMAGE := $(BOOTLOADER_DIR)/build/bootloader.bin

# This rule hook is defined in the ChibiOS build system
POST_MAKE_ALL_RULE_HOOK: build/$(PROJECT).bin build/$(PROJECT).elf
	# Building the bootloader
	+cd $(BOOTLOADER_DIR) && make -j8

	# Removing previous build outputs that could use a different git hash
	rm -rf build/*.uavcan.bin build/*.compound.bin

	# Generating compound image with embedded bootloader
	cd build && dd if=/dev/zero bs=$(BOOTLOADER_SIZE) count=1 | tr "\000" "\377" >padded_bootloader.tmp.bin
	cd build && dd if=$(BOOTLOADER_IMAGE) of=padded_bootloader.tmp.bin conv=notrunc
	cd build && cat padded_bootloader.tmp.bin $(PROJECT).bin >$(COMPOUND_IMAGE_FILE)

	cd build && $(BOOTLOADER_DIR)/../tools/kocherga_image.py $(PROJECT).bin\
															 --side-patch $(PROJECT).elf    \
															 --side-patch $(COMPOUND_IMAGE_FILE)
	# Generating the signed image for the bootloader
	#cd build && ../zubax_chibios/tools/make_boot_descriptor.py $(PROJECT).bin $(PROJECT) $(HW_VERSION_MAJOR)       \
	#                                                           --also-patch-descriptor-in=$(PROJECT).elf           \
	#                                                           --also-patch-descriptor-in=$(COMPOUND_IMAGE_FILE)

	# Injecting the bootloader into the final ELF; note that we're using unpadded bootloader to preserve signature
	cd build && $(TOOLCHAIN_PREFIX)-objcopy --add-section bootloader=$(BOOTLOADER_IMAGE)   \
	                                        --set-section-flags bootloader=load,alloc      \
	                                        --change-section-address bootloader=0x08000000 \
	                                        $(PROJECT).elf compound.elf

	# Removing temporary files
	cd build && rm -f $(PROJECT).bin $(PROJECT).elf *.hex *.tmp.bin

$(COMMON_SETTINGS_INCLUDED_LINKER_FILE_PATH): ../linker_script_settings.ld.settings
	@rm -f $(COMMON_SETTINGS_INCLUDED_LINKER_FILE_PATH)
	@echo "/* This file was created by the Makefile in the firmware folder */\n\n"> $(COMMON_SETTINGS_INCLUDED_LINKER_FILE_PATH)
	@cat $(SAPOG_SRC_DIR)/../../linker_script_settings.ld.settings >> $(COMMON_SETTINGS_INCLUDED_LINKER_FILE_PATH)
	@echo "\n\n">> $(COMMON_SETTINGS_INCLUDED_LINKER_FILE_PATH)
	@cat $(SAPOG_SRC_DIR)/../linker.ld >> $(COMMON_SETTINGS_INCLUDED_LINKER_FILE_PATH)
	@echo "Created a combined linker file for the firmware"

	@rm -f $(COMMON_SETTINGS_INCLUDED_BOOTLOADER_LINKER_FILE_PATH)
	@echo "/* This file was created by the Makefile in the firmware folder */\n\n"> $(COMMON_SETTINGS_INCLUDED_BOOTLOADER_LINKER_FILE_PATH)
	@cat $(SAPOG_SRC_DIR)/../../linker_script_settings.ld.settings >> $(COMMON_SETTINGS_INCLUDED_BOOTLOADER_LINKER_FILE_PATH)
	@echo "\n\n">> $(COMMON_SETTINGS_INCLUDED_BOOTLOADER_LINKER_FILE_PATH)
	@cat $(SAPOG_SRC_DIR)/../../bootloader/ld.ld >> $(COMMON_SETTINGS_INCLUDED_BOOTLOADER_LINKER_FILE_PATH)
	@echo "Created a combined linker file for the bootloader"

upload: build/compound.elf
	./zubax_chibios/tools/blackmagic_flash.sh

# DSDL related rules

clean_previous_zip:
	rm -f master.zip*

clean_previous_unpacked_folder:
	rm -rf public_regulated_data_types-master
public_regulated_data_types-master:
	@wget https://github.com/UAVCAN/public_regulated_data_types/archive/refs/heads/master.zip -q && echo "Downloaded master.zip"
	@unzip -n master.zip > /dev/null && echo "Unpacked master.zip into the firmware folder"
	@rm -f master.zip*

public_regulated_data_types: public_regulated_data_types-master
	mkdir -p public_regulated_data_types
	mv -v public_regulated_data_types-master/** public_regulated_data_types/
	rm -rf public_regulated_data_types-master

generated/nunavut_out: public_regulated_data_types
	@echo "Compiling C DSDL for UAVCAN, first for the reg folder, which includes uavcan"
	nnvg public_regulated_data_types/reg -e h -O generated/nunavut_out -I public_regulated_data_types/uavcan
	@echo "Compiling C DSDL for UAVCAN, first for the uavcan folder, which includes reg"
	nnvg public_regulated_data_types/uavcan -e h -O generated/nunavut_out -I public_regulated_data_types/reg

dsdl: clean_previous_zip clean_previous_unpacked_folder generated/nunavut_out;

include zubax_chibios/rules_stm32f105_107.mk
