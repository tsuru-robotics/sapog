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
    flash : org = 0x08000000, len = 57088 /* 32512 32K for the bootloader minus 256 for the signature */

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
    ram   : org = 0x20000140, len = 65280 /* First 256 bytes are reserved for bootloader/app communication and the next 64 are for its CRC */
}


__ram_start__          = ORIGIN(ram);
__ram_size__           = LENGTH(ram);
__ram_end__            = __ram_start__ + __ram_size__;

ENTRY(Reset_Handler)

PROVIDE(DeviceSignatureStorage = 0x0800E000);
PROVIDE(AppSharedStruct = 0x20000000);

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
    } > flash

    constructors : ALIGN(4) SUBALIGN(4)
    {
        FILL(0xDEADC0DE);
        PROVIDE(__init_array_start = .);
        KEEP(*(SORT(.init_array.*)))
        KEEP(*(.init_array))
        PROVIDE(__init_array_end = .);
    } > flash

    destructors : ALIGN(4) SUBALIGN(4)
    {
        FILL(0xDEADC0DE);
        PROVIDE(__fini_array_start = .);
        KEEP(*(.fini_array))
        KEEP(*(SORT(.fini_array.*)))
        PROVIDE(__fini_array_end = .);
    } > flash

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
    } > flash

    .ARM.extab :
    {
        *(.ARM.extab* .gnu.linkonce.armextab.*)
    } > flash

    .ARM.exidx :
    {
        PROVIDE(__exidx_start = .);
        *(.ARM.exidx* .gnu.linkonce.armexidx.*)
        PROVIDE(__exidx_end = .);
     } > flash

    .eh_frame_hdr :
    {
        *(.eh_frame_hdr)
    } > flash

    .eh_frame : ONLY_IF_RO
    {
        *(.eh_frame)
    } > flash

    .textalign : ONLY_IF_RO
    {
        FILL(0xDEADC0DE);
        BYTE(0xFF);
        . = ALIGN(64);
    } > flash

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
}

/* Heap default boundaries, it is defaulted to be the non-used part of ram region.*/
__heap_base__   = __ram_free__;
__heap_end__    = __ram_end__;

