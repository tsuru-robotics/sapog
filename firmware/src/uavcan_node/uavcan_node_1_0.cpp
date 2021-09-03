/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#include "uavcan_node_1_0.hpp"
#include "zubax_chibios/sys/sys.hpp"
//#include "chthreads.h"
#include <cstddef>
#include "zubax_chibios/config/config.hpp"
#include "zubax_chibios/platform/stm32/config_storage.hpp"
/*#include "chcore.h"
#include "chtypes.h"
#include "chschd.h"*/

#include <ch.h>
namespace board{
    extern void die(int error);
    extern void* const ConfigStorageAddress;
    constexpr unsigned ConfigStorageSize = 1024;
}
using namespace uavcan_node_1_0;
using namespace board;
static THD_WORKING_AREA(_wa_control_thread, 1024); // This defines _wa_control_thread
static void control_thread(void* arg)
{
    (void) arg;
    chRegSetThreadName("heartbeat_control_thread");
    //event_listener_t listener;
    //chEvtRegisterMask(&_setpoint_update_event, &listener, ALL_EVENTS);

    //uint64_t timestamp_hnsec = motor_rtctl_timestamp_hnsec();
    while (1) {

    }
}
int UAVCANNode::init(){
    static os::stm32::ConfigStorageBackend config_storage_backend(ConfigStorageAddress, ConfigStorageSize);
    const int config_init_res = os::config::init(&config_storage_backend);
    if (config_init_res < 0)
    {
        die(config_init_res);
    }
    if (!chThdCreateStatic(_wa_control_thread, sizeof(_wa_control_thread), HIGHPRIO - 1, control_thread, NULL)) { // HIGHPRIO from #include "chschd.h"
        return -1;
    }
    return 0;
}
