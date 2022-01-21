/// Copyright (c) 2016-2017  Zubax Robotics  <info@zubax.com>

#pragma once

#include "mcuconf.h"

#define HAL_USE_PAL                         TRUE
#define HAL_USE_ADC                         FALSE
#define HAL_USE_CAN                         FALSE
#define HAL_USE_CRY                         FALSE
#define HAL_USE_DAC                         FALSE
#define HAL_USE_EXT                         FALSE
#define HAL_USE_GPT                         FALSE
#define HAL_USE_I2C                         FALSE
#define HAL_USE_I2S                         FALSE
#define HAL_USE_ICU                         FALSE
#define HAL_USE_MAC                         FALSE
#define HAL_USE_MMC_SPI                     FALSE
#define HAL_USE_PWM                         FALSE
#define HAL_USE_QSPI                        FALSE
#define HAL_USE_RTC                         FALSE
#define HAL_USE_SDC                         FALSE
#define HAL_USE_SERIAL                      TRUE
#define HAL_USE_SERIAL_USB                  FALSE
#define HAL_USE_SPI                         FALSE
#define HAL_USE_UART                        FALSE
#define HAL_USE_USB                         FALSE
#define HAL_USE_WDG                         FALSE

// PAL driver related settings.
#define PAL_USE_CALLBACKS                   FALSE
#define PAL_USE_WAIT                        FALSE

// SERIAL driver related settings.
#define SERIAL_DEFAULT_BITRATE              921600
#define SERIAL_BUFFERS_SIZE                 2048

// SERIAL_USB driver related setting.
#define SERIAL_USB_BUFFERS_SIZE             2048
#define SERIAL_USB_BUFFERS_NUMBER           2

// USB driver related settings.
#define USB_USE_WAIT                        TRUE