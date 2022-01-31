/*
 * Copyright (C) 2015  Zubax Robotics  <info@zubax.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Author: Pavel Kirienko <pavel.kirienko@zubax.com>
 */

 /*
  * Based on a ChibiOS demo app.
  */

__main_stack_size__     = 0x0800;
__process_stack_size__  = 0x0800;

MEMORY
{
    flash : org = 0x0800E400, len = 204800 /* 223k 32K for bootloader, 1K for configs */
    ram   : org = 0x20000100, len = 65280 /* 64K - 256 for AppShared struct */
}


__ram_start__          = ORIGIN(ram);
__ram_size__           = LENGTH(ram);
__ram_end__            = __ram_start__ + __ram_size__;

ENTRY(Reset_Handler)

PROVIDE(DeviceSignatureStorage = ORIGIN(flash) - 256);

SECTIONS
{
    . = 0;
    _text = .;

    startup : ALIGN(16) SUBALIGN(16)
    {
        KEEP(*(.vectors))
        . = ALIGN(8);
        KEEP(*(.app_descriptor));
        . = ALIGN(8);
    } > flash

    constructors : ALIGN(4) SUBALIGN(4)
    {
        PROVIDE(__init_array_start = .);
        KEEP(*(SORT(.init_array.*)))
        KEEP(*(.init_array))
        PROVIDE(__init_array_end = .);
    } > flash

    destructors : ALIGN(4) SUBALIGN(4)
    {
        PROVIDE(__fini_array_start = .);
        KEEP(*(.fini_array))
        KEEP(*(SORT(.fini_array.*)))
        PROVIDE(__fini_array_end = .);
    } > flash

    /*
     * This padding section must be inserted before every section with greater alignment.
     */
    .padding1 :
    {
        /*
         * Filling is important: if it is not specified, gaps between aligned sections will be filled with zero when
         * exporting binaries, and will be skipped (i.e. set to 0xFF) when flashing .elf directly during debugging.
         * The discrepancy causes the firmware CRC to mismatch, preventing the bootloader from running it.
         * Assigning a well-defined fill byte eliminates the discrepancy (binary files will also contain 0xFF),
         * allowing to flash the firmware directly with an SWD debugger during development.
         * See http://www.math.utah.edu/docs/info/ld_3.html
         */
        FILL(0xFF);
        . += 1;            /* This increment prevents moving location counter backwards if no alignment is needed */
        . = ALIGN(16) - 1;
        BYTE(0xFF)         /* Without this, the linker will ignore alignment */
    } > flash

    .text : ALIGN(16) SUBALIGN(16)
    {
        FILL(0x99);
        *(.text)
        *(.text.*)
        *(.rodata)
        *(.rodata.*)
        BYTE(0xFF)
        . = ALIGN(16);
        *(.glue_7t)
        *(.glue_7)
        *(.gcc*)
    } > flash

    .ARM.extab : ALIGN(16) SUBALIGN(16)
    {
        *(.ARM.extab* .gnu.linkonce.armextab.*)
    } > flash

    .ARM.exidx : ALIGN(16) SUBALIGN(16)
    {
        PROVIDE(__exidx_start = .);
        *(.ARM.exidx* .gnu.linkonce.armexidx.*)
        PROVIDE(__exidx_end = .);
     } > flash

    .eh_frame_hdr : ALIGN(16) SUBALIGN(16)
    {
        *(.eh_frame_hdr)
    } > flash

    .eh_frame : ONLY_IF_RO
    {
        *(.eh_frame)
    } > flash

    .textalign : ONLY_IF_RO
    {
        . = ALIGN(8);
    } > flash

    . = ALIGN(4);
    _etext = .;
    _textdata_start = _etext;

    .mstack : ALIGN(16) SUBALIGN(16)
    {
        . = ALIGN(8);
        __main_stack_base__ = .;
        . += __main_stack_size__;
        . = ALIGN(8);
        __main_stack_end__ = .;
    } > ram

    .pstack : ALIGN(16) SUBALIGN(16)
    {
        __process_stack_base__ = .;
        __main_thread_stack_base__ = .;
        . += __process_stack_size__;
        . = ALIGN(8);
        __process_stack_end__ = .;
        __main_thread_stack_end__ = .;
    } > ram

    .data : ALIGN(4)
    {
        . = ALIGN(4);
        PROVIDE(_data_start = .);
        *(.data)
        *(.data.*)
        *(.ramtext)
        . = ALIGN(4);
        PROVIDE(_data_end = .);
    } > ram AT > flash

    .bss : ALIGN(4)
    {
        . = ALIGN(4);
        PROVIDE(_bss_start = .);
        *(.bss)
        *(.bss.*)
        *(COMMON)
        . = ALIGN(4);
        PROVIDE(_bss_end = .);
        PROVIDE(end = .);
    } > ram

    .ram (NOLOAD) : ALIGN(4)
    {
        . = ALIGN(4);
        *(.ram)
        *(.ram.*)
        . = ALIGN(4);
        __ram_free__ = .;
    } > ram
    . = ALIGN(16);  /* Heap allocators require large alignment (e.g., O1Heap). */
    __heap_base__ = .;
    __heap_end__ = __ram_end__;
    /* The bootloader shared struct may be occluded by heap by design. This is because it is not needed normally. */
    __bootloader_io = (__ram_end__ - 512);
}

