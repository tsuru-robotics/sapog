/* This file was created by the Makefile in the firmware folder */


/* SETTINGS START FROM linker_script_settings.ld.settings */
"flash_start_address" = 0x8000000;
"flash_page_size" = 2048;
"bootloader_size_pages" = 16;
"bootloader_size_B" = bootloader_size_pages * flash_page_size;
/* The app also starts on this page right after the 256 bytes */
"DeviceSignatureStorage_start_address" = flash_start_address + bootloader_size_B;
"DeviceSignatureStorage_size" = 256;
/* Addresses of important locations */
/* The Application starts on the next page after the page that the DeviceSignature happened to be on */
/* The application needs its own page because erasing is done page by page */
"Application_start_address" = (DeviceSignatureStorage_start_address / flash_page_size + 1) * flash_page_size;
/* SETTINGS END */
/* You can use arm-none-eabi-readelf -all -W build/compound.elf | grep "Appl\|Device\|flash_\|bootloader_" to read the values of these when they end up in the ELF file as symbols*/



/**
 * Copyright (c) 2016  Zubax Robotics  <info@zubax.com>
 */
MEMORY
{
    /*
     * Location of the signature can't be easily changed because that would break
     * binary compatibility with released firmware images.
     *
     *  Start        End      Size      Purpose
     * ----------------------------------------------------
     *      0      32512      32512     Bootloader
     *  32512      32768        256     Digital signature
     *  32768                           Application
     */
    bootloader_flash : org = 0x08000000, len = 59136  /* 32512 32K for the bootloader minus 256 for the signature */

    /*
     * We use both SRAM1 and SRAM2 as a single contiguous memory region.
     * The very end of SRAM2 is used for app-bootloader communication.
     *
     *  Start        End      Size      Purpose
     * ----------------------------------------------------
     *      0        256       256    Space for application-bootloader data exchange -- legacy
     *    256     130560    130304    Bootloader
     * 130560       128K       512    Space for application-bootloader data exchange
     */
    ram   : org = 0x20000000, len = 65265 /* 64K - 263 - 8 for AppShared */
}

__ram_start__          = ORIGIN(ram);
__ram_size__           = LENGTH(ram);
__ram_end__            = __ram_start__ + __ram_size__;

ENTRY(Reset_Handler);


/*
   The DeviceSignature is not actually used at this moment.
   If it was used then it would erase the application if the signature was missing or invalid.
*/
PROVIDE(DeviceSignatureStorage = "DeviceSignatureStorage_start_address");
PROVIDE(AppSharedStruct = 0x2000FEF0); /* I honestly don't remember how I got this address. It's supposed to be at the very end of RAM 0x20010000 - 256 */

SECTIONS
{

    . = 0;
    _text = .;

    startup : ALIGN(16) SUBALIGN(16)
    {
        FILL(0xDEADC0DE);
        KEEP(*(.vectors))
        . = ALIGN(8);
        KEEP(*(.app_descriptor));
        . = ALIGN(8);
    } > bootloader_flash

    constructors : ALIGN(4) SUBALIGN(4)
    {
        FILL(0xDEADC0DE);
        PROVIDE(__init_array_start = .);
        KEEP(*(SORT(.init_array.*)))
        KEEP(*(.init_array))
        PROVIDE(__init_array_end = .);
    } > bootloader_flash

    destructors : ALIGN(4) SUBALIGN(4)
    {
        FILL(0xDEADC0DE);
        PROVIDE(__fini_array_start = .);
        KEEP(*(.fini_array))
        KEEP(*(SORT(.fini_array.*)))
        PROVIDE(__fini_array_end = .);
    } > bootloader_flash

    .text : ALIGN(4) SUBALIGN(4)
    {
        FILL(0xDEADC0DE);
        *(.text)
        *(.text.*)
        *(.rodata)
        *(.rodata.*)
        *(.glue_7t)
        *(.glue_7)
        *(.gcc*)
        /*
         * Note that SOME DEBUGGERS WILL REFUSE TO LOAD THE ELF if it contains odd-sized sections!
         * This issue can be observed, for example, with DroneCode Probe.
         * It also important to ensure proper alignment at the end of the section in order to
         * avoid gaps that contain undefined bytes (see the padding sections for details).
         */
        . = ALIGN(8);
    } > bootloader_flash

    .ARM.extab :
    {
        *(.ARM.extab* .gnu.linkonce.armextab.*)
    } > bootloader_flash

    .ARM.exidx :
    {
        PROVIDE(__exidx_start = .);
        *(.ARM.exidx* .gnu.linkonce.armexidx.*)
        PROVIDE(__exidx_end = .);
     } > bootloader_flash

    .eh_frame_hdr :
    {
        *(.eh_frame_hdr)
    } > bootloader_flash

    .eh_frame : ONLY_IF_RO
    {
        *(.eh_frame)
    } > bootloader_flash

    .textalign : ONLY_IF_RO
    {
        FILL(0xDEADC0DE);
        BYTE(0xFF);
        . = ALIGN(64);
    } > bootloader_flash

    . = ALIGN(4);
    _etext = .;
    _textdata_start = _etext;

    .mstack :
    {
        . = ALIGN(8);
        __main_stack_base__ = .;
        . += __main_stack_size__;
        . = ALIGN(8);
        __main_stack_end__ = .;
    } > ram

    .pstack :
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
        FILL(0xDEADC0DE);
        . = ALIGN(4);
        PROVIDE(_data_start = .);
        *(.data)
        *(.data.*)
        *(.ramtext)
        . = ALIGN(4);
        PROVIDE(_data_end = .);
    } > ram AT > bootloader_flash

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
}

/* Heap default boundaries, it is defaulted to be the non-used part of ram region.*/
__heap_base__   = __ram_free__;
__heap_end__    = __ram_end__;

