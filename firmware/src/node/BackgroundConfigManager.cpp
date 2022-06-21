#include "BackgroundConfigManager.hpp"
#include "zubax_chibios/sys/sys.hpp"
#include "motor/motor.hpp"
#include <stdio.h>

void BackgroundConfigManager::poll() {
    const auto new_mod_cnt = os::config::getModificationCounter();

    if (new_mod_cnt != modification_counter_)
    {
        modification_counter_ = new_mod_cnt;
        last_modification_ts_ = chVTGetSystemTimeX();
        pending_save_ = true;
    }

    if (pending_save_)
    {
        if (getTimeSinceModification() > (last_save_failed_ ? SaveDelayAfterError : SaveDelay))
        {
            os::TemporaryPriorityChanger priority_changer(HIGHPRIO);
            if (motor_is_idle())
            {
                printf("Saving config...\n");
                const int res = configSave();
                if (res >= 0)
                {
                    pending_save_ = false;
                    last_save_failed_ = false;
                } else
                {
                    last_save_failed_ = true;
                }
            }
        }
    }
}

float BackgroundConfigManager::getTimeSinceModification() const {
    return float(ST2MS(chVTTimeElapsedSinceX(last_modification_ts_))) / 1e3F;
}
