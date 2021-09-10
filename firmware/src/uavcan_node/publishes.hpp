#ifndef FIRMWARE_PUBLISHES_HPP
#define FIRMWARE_PUBLISHES_HPP

#include "units.hpp"
#include "node_state.h"
#include "transmission.h"
#include <iterator>

namespace node
{
    namespace communications
    {
        using namespace state;

        void publish_port_list(CanardInstance &canard, State &state)
        {
            assert(canard.node_id > CANARD_NODE_ID_MAX);
            uavcan_node_port_List_0_1 m{};
            uavcan_node_port_List_0_1_initialize_(&m);
            uavcan_node_port_SubjectIDList_0_1_select_sparse_list_(&m.publishers);
            uavcan_node_port_SubjectIDList_0_1_select_sparse_list_(&m.subscribers);
            // Indicate which subjects we publish to. Don't forget to keep this updated if you add new publications!
            {
                size_t *const cnt = &m.publishers.sparse_list.count;
                m.publishers.sparse_list.elements[(*cnt)++].value = uavcan_node_Heartbeat_1_0_FIXED_PORT_ID_;
                m.publishers.sparse_list.elements[(*cnt)++].value = uavcan_node_port_List_0_1_FIXED_PORT_ID_;
                // TODO: implement subscriptions
            }

            // Indicate which servers and subscribers we implement.
            // We could construct the list manually but it's easier and more robust to just query libcanard for that.
            const CanardRxSubscription *rxs = canard._rx_subscriptions[CanardTransferKindMessage];
            while (rxs != NULL)
            {
                m.subscribers.sparse_list.elements[m.subscribers.sparse_list.count++].value = rxs->_port_id;
                rxs = rxs->_next;
            }
            rxs = canard._rx_subscriptions[CanardTransferKindRequest];
            while (rxs != NULL)
            {
                nunavutSetBit(&m.servers.mask_bitpacked_[0], sizeof(m.servers.mask_bitpacked_), rxs->_port_id, true);
                rxs = rxs->_next;
            }
            // Notice that we don't check the clients because our application doesn't invoke any services.

            // Serialize and publish the message. Use a small buffer because we know that our message is always small.
            uint8_t serialized[512] = {0};  // https://github.com/UAVCAN/nunavut/issues/191
            size_t serialized_size = uavcan_node_port_List_0_1_SERIALIZATION_BUFFER_SIZE_BYTES_;
            if (uavcan_node_port_List_0_1_serialize_(&m, &serialized[0], &serialized_size) >= 0)
            {
                const CanardTransfer transfer = {
                        .timestamp_usec = state.timing.current_time + MEGA,
                        .priority       = CanardPriorityOptional,  // Mind the priority.
                        .transfer_kind  = CanardTransferKindMessage,
                        .port_id        = uavcan_node_port_List_0_1_FIXED_PORT_ID_,
                        .remote_node_id = CANARD_NODE_ID_UNSET,
                        .transfer_id    = (CanardTransferID) (state.transfer_ids.uavcan_node_port_list++),
                        .payload_size   = serialized_size,
                        .payload        = &serialized[0],
                };
                (void) canardTxPush(&canard, &transfer);
            }
        }

        void publish_heartbeat(CanardInstance &canard, State &state)
        {
            uavcan_node_Heartbeat_1_0 heartbeat{};
            heartbeat.uptime = (uint32_t) ((state.timing.current_time - state.timing.started_at) / MEGA);
            heartbeat.mode.value = uavcan_node_Mode_1_0_OPERATIONAL;
            heartbeat.health.value = uavcan_node_Health_1_0_NOMINAL;
            uint8_t serialized[uavcan_node_Heartbeat_1_0_SERIALIZATION_BUFFER_SIZE_BYTES_]{};
            size_t serialized_size = sizeof(serialized);
            const int8_t err = uavcan_node_Heartbeat_1_0_serialize_(&heartbeat, &serialized[0], &serialized_size);
            assert(err >= 0);
            if (err >= 0)
            {
                const CanardTransfer transfer = {
                        .timestamp_usec = state.timing.current_time +
                                          MEGA, // transmission deadline 1 second, optimal for heartbeat
                        .priority       = CanardPriorityNominal,
                        .transfer_kind  = CanardTransferKindMessage,
                        .port_id        = uavcan_node_Heartbeat_1_0_FIXED_PORT_ID_,
                        .remote_node_id = CANARD_NODE_ID_UNSET,
                        .transfer_id    = (CanardTransferID) (state.transfer_ids.uavcan_node_heartbeat++),
                        .payload_size   = serialized_size,
                        .payload        = &serialized[0],
                };
                (void) canardTxPush(&canard, &transfer);
            }
            transmit(state);
        }
    }
}


#endif //FIRMWARE_PUBLISHES_HPP
