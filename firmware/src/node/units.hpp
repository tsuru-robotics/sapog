/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#define KILO 1000L
#define MEGA ((int64_t) KILO * KILO)
#define SECOND_IN_MICROSECONDS MEGA
#define QUEUE_TIME_FRAME 100 // once every 100 microseconds
#define ONE_SECOND_DEADLINE_usec 1000000