#ifndef UAVCAN_EQUIPMENT_ARMING_STATUS_MONITOR_HPP_INCLUDED
#define UAVCAN_EQUIPMENT_ARMING_STATUS_MONITOR_HPP_INCLUDED

#include <uavcan/debug.hpp>
#include <uavcan/util/method_binder.hpp>
#include <uavcan/node/subscriber.hpp>
#include <uavcan/equipment/safety/ArmingStatus.hpp>
#include <cassert>
#include <cstdlib>

namespace uavcan
{
    class UAVCAN_EXPORT ArmingStatusMonitor
            {
            public:
                    explicit ArmingStatusMonitor(INode& node): _sub(node) { }
                    virtual ~ArmingStatusMonitor() { }

                    int start()
                    {
                        const int res = _sub.start(ArmingStatusCallback(this, &ArmingStatusMonitor::handleArmingStatus));
                        if (res != 0) {
                            printf("ArmingStatus sub failed %i", res);
                        }
                        return res;
                    }

                    uint8_t getArmingStatus() const
                    {
                        return _arming_status;
                    }

            private:
                    typedef MethodBinder<ArmingStatusMonitor*,
                    void (ArmingStatusMonitor::*)(const ReceivedDataStructure<equipment::safety::ArmingStatus>&)>
                    ArmingStatusCallback;

                    Subscriber<equipment::safety::ArmingStatus, ArmingStatusCallback> _sub;

                    mutable uint8_t _arming_status{uavcan::equipment::safety::ArmingStatus::STATUS_DISARMED};

                    void handleArmingStatus(const ReceivedDataStructure<equipment::safety::ArmingStatus>& msg)
                    {
                        _arming_status = msg.status;
                    }
            };

}

#endif // UAVCAN_EQUIPMENT_ARMING_STATUS_MONITOR_HPP_INCLUDED
