# Interfaces

## Standard ESC interface

Ensure conformance with:

https://github.com/UAVCAN/public_regulated_data_types/blob/8e24ae6d6414f4e047415ab1dc440dd7263d45ee/reg/udral/service/actuator/esc/_.0.1.uavcan

As in the demo, the registers which define the port numbers for every subject are configured. When a new component is inserted into a system, it has to be configured to determine, how it is supposed to be connected to the rest of the system.

One possible solution is making glue logic between the configuration parameter storage and a lookup table of lambdas.

Most of the configuration parameters will need to be renamed to be compatible with the UAVCAN standard.


## Interface for sound emission

In the process of sound emission, a motor is excited with a high current to make the coils oscillate at a high frequency.

https://github.com/Zubax/sapog/blob/601f4580b71c3c4da65cc52237e62a163d6a6a16/firmware/src/motor/motor.c#L719-L731

A subscriber should be implemented for the subject of https://github.com/UAVCAN/public_regulated_data_types/blob/udral/reg/udral/physics/acoustics/Note.0.1.uavcan

The acoustic power parameter should be ignored because Sapog doesn't provide an API for controlling it.


# A set of service functions


## Bitrate detection

Has a configuration parameter for CAN bus bitrate. The default value should be unconfigured. If the value is missing then the firmware should detect the bitrate automatically.

https://github.com/Zubax/sapog/blob/601f4580b71c3c4da65cc52237e62a163d6a6a16/firmware/src/motor/motor.c#L719-L731
natural132[2] (second item) should be ignored

We use classic CAN
https://www.kvaser.com/wp-content/uploads/2016/10/comparing-can-fd-with-classical-can.pdf

## Plug and play (PNP) nodeid allocation

Demo implementation: https://github.com/UAVCAN/demos/blob/main/ds015_servo/src/main.c#L341-L373

A register is needed for the nodeid to be stored, use standard: https://github.com/UAVCAN/public_regulated_data_types/blob/udral/uavcan/register/384.Access.1.0.uavcan

We use Yakut at the moment for configuring:
https://github.com/UAVCAN/yakut/issues/3

If the value is configured by an integrator, the person integrating the device into the vehicle, then that is used, else, it is automatically determined.

## Node info request

https://github.com/UAVCAN/public_regulated_data_types/blob/8e24ae6d6414f4e047415ab1dc440dd7263d45ee/uavcan/node/430.GetInfo.1.0.uavcan

Handling the request:
https://github.com/UAVCAN/demos/blob/main/ds015_servo/src/main.c#L675-L695

Getting the info:
https://github.com/UAVCAN/demos/blob/main/ds015_servo/src/main.c#L615-L637

## Node ports list

Periodically publishing a list of subjects and services that the node interacts with.

Demo implementation:
https://github.com/UAVCAN/demos/blob/main/ds015_servo/src/main.c#L413-L481


## Execute command

uavcan.node.ExecuteCommand

COMMAND_RESTART

COMMAND_BEGIN_SOFTWARE_UPDATE

will do nothing for now, because we are still using the old bootloader

COMMAND_FACTORY_RESET

this will erase the config, there is a function for that: zubax_chibios/config.h line 69 configErase


## It should use both CAN interfaces for redundancy

Use libcanard v2.

The API in this libcanard version is slightly different because it is built to use two
CAN interfaces for redundancy.

1. canardTxPush will propagate every frame into two transmission queues.
2. when you read the transmission queue you need to specify, which queue you read
3. other differences too.


## Use nunavut to generate the files automatically

There is a need to generate with Nunavut automatically from the make file.


## Memory management

In a practical application, the array that is currently used for o1heap in branch silver-heartbeat-thread should be replaced with all of the unused memory. Can be done by modifying the linker script.