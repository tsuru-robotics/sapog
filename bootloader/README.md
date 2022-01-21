Sapog bootloader
=================

This is a bootloader adapted for use with Sapog.

## Operating principles

The bootloader does not have the frequency auto-detection capability for reasons of simplicity;
instead, it relies on the firmware to detect the frequency and store its value in megahertz in the first byte
of the OTP flash area; the value shall be a multiple of four [megahertz].
Obviously, during the first boot there will be no frequency stored in the OTP, the same is true if the firmware
lacks that capability; in this case the bootloader will continue using the HSI oscillator.
Due to its large frequency drift, CAN is not expected to work reliably when clocked from HSI.

The bootloader is based on [Kocherga](https://github.com/Zubax/kocherga).
The RGB LED is used to indicate states as follows (always solid, never blinking):

- **Cyan**    -- The bootloader is starting, initial checks in progress.
- **Green**   -- The bootloader is idle, waiting for command; the application is valid.
- **Blue**    -- A new application image is being downloaded and verified.
- **Yellow**  -- No valid application is available to boot, waiting for command.
- **Red**     -- Critical hardware or software failure. The device will be reset by the watchdog timer.
- (dark)      -- Application is being started (transient) or failed to start (persistent).

The bootloader is optimized to boot the application ASAP if it is valid.
This is done to minimize the downtime in case of an in-the-air reboot.
Interfaces are not initialized in the case of such fast-track boot-up.

Local node-ID is auto-allocated if not supplied by the application.

You will find the definition of the app-shared struct (that is passed from the application to the bootloader)
under `/src/`.
The bootloader may also recognize legacy app-shared structures to ensure compatibility with old versions of
the application firmware.

Kocherga is designed to run in a single-threaded environment, so the entire bootloader is operated from the main
thread only by calling `kocherga::Bootloader::poll()` approx. every 100 microseconds.
Deviations are possible when the ROM backend needs to erase the next sector of flash, etc.
On the following diagram, the top plot represents bootloader activity, the bottom is high when the core is idling:

![execution logic trace](/docs/execution-logic-trace.png)

### UAVCAN/CAN

A UAVCAN/CAN node that supports both v1 and v0 with automatic protocol version detection operates via CAN1.
CAN2 is not used; therefore, Sapog-based hardware that only leverages one CAN bus interface shall use CAN1, not CAN2.

If bitrate is not supplied by the application, it is detected automatically from the four standard values prescribed
by UCANPHY v1.0.

The CAN bootloader can be operated manually using the legacy UAVCAN GUI Tool (UAVCAN v0),
or using the Yakut CLI tool (UAVCAN v1) similar to the UAVCAN/serial case.
If you want to use Yakut with SocketCAN, the environment variables would be roughly as follows:

```bash
UAVCAN__CAN__IFACE=socketcan:slcan0  # Whatever interface you need (not necessarily slcan).
UAVCAN__CAN__MTU=8
UAVCAN__CAN__BITRATE=1000000
UAVCAN__NODE__ID=127                 # Choose any unoccupied node-ID for Yakut.
```

If you prefer to connect directly to the Babel port (or any other SLCAN adapter) bypassing SocketCAN,
replace `UAVCAN__CAN__IFACE` with `slcan:/dev/serial/...`.
If you are using SLCAN with SocketCAN, there is a helper script `setup_slcan` that can be found at
<https://gist.github.com/pavel-kirienko/32e395683e8b7f49e71413aebf5e1a89>:

```bash
$ sudo setup_slcan --remove-all /dev/serial/by-id/usb-Zubax_Robotics_Zubax_Babel_21003D00145130365030332000000000-if00
```

The following screenshot shows the update via CAN in progress with concurrent monitoring of its status via UART
(in the bottom-left terminal):

![update tools demo](/docs/update-tools-demo.png)

## Development

Please refer to the main application firmware documentation for development instructions.
The recommended IDE is JetBrains CLion.

Use `format.sh` to apply automatic code formatting using Clang-Format.
Better yet, configure CLion to do that automatically.

In order to build the bootloader, execute `make RELEASE=1`.
Omit setting the `RELEASE` variable to build the debug version (it may not fit into the bootloader area).

Testing shall be performed manually.
This is acceptable for this project since it does not require continuous on-going development.

### Releasing

Once the release version of the bootloader is built,
its binary (`.bin`) will have to be manually copied to the destination tree,
whether it's another repository or the Zubax file server, depending on the workflow.
This is arranged this way to ensure that once a working version of bootloader is finished and tested,
it will stay frozen in this exact configuration until updated explicitly.
The bootloader has to be robust and is not expected to change frequently.

## MCU Usage

### Communication interfaces

| Peripheral | Usage                                      |
|------------|--------------------------------------------|
| UART3      | Main and only UART port with UAVCAN/serial |
| USB        | USB CDC ACM with UAVCAN/serial             |
| CAN1       | UAVCAN/CAN                                 |

### Timers

The following list documents the current usage of hardware timers.
All timers are clocked at 180 MHz.

| Timer | Resolution | Usage                        |
|-------|------------|------------------------------|
| TIM1  | 16         | *Not used*                   |
| TIM2  | **32**     | RTOS System Timer (tickless) |
| TIM3  | 16         | RGB LED PWM                  |
| TIM4  | 16         | *Not used*                   |
| TIM5  | **32**     | *Not used*                   |
| TIM6  | 16         | *Not used*                   |
| TIM7  | 16         | *Not used*                   |
| TIM8  | 16         | *Not used*                   |
| TIM9  | 16         | *Not used*                   |
| TIM10 | 16         | *Not used*                   |
| TIM11 | 16         | *Not used*                   |
| TIM12 | 16         | *Not used*                   |
| TIM13 | 16         | *Not used*                   |
| TIM14 | 16         | *Not used*                   |

### Watchdog

The bootloader initializes the watchdog with a large timeout.
This is needed to prevent broken firmwares from bricking the device.

### RCC

The RCC CSR register contains reset cause flags.
If either of the watchdog timers is known to have caused the last reset,
the bootloader will inject a 10 second timeout before booting the application,
allowing external systems or the user to intervene and replace the bad firmware.
The reset cause flags are cleared by the bootloader.
