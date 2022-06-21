#pragma once

#include "ch.h"
#include "zubax_chibios/config/config.hpp"

/**
 * Managing configuration parameters in the background from the main thread.
 * This code was borrowed from PX4ESC.
 */
class BackgroundConfigManager
{
    static constexpr float SaveDelay = 1.0F;
    static constexpr float SaveDelayAfterError = 10.0F;
    unsigned modification_counter_ = os::config::getModificationCounter();
    ::systime_t last_modification_ts_ = chVTGetSystemTimeX();
    bool pending_save_ = false;
    bool last_save_failed_ = false;
    float getTimeSinceModification() const;
public:
    void poll();
};
