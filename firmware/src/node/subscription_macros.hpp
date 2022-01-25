#pragma once

#include "libcanard/canard.h"

/* These macros depend on one another, here is how one requires another to save you time looking through the code:
 * CONFIGURABLE_ID_MESSAGE_SUBSCRIPTION -> CONFIGURABLE_ID_SUBSCRIPTION -> ANY_SUBSCRIPTION
 * CONFIGURABLE_ID_SERVICE_SUBSCRIPTION -> CONFIGURABLE_ID_SUBSCRIPTION -> ANY_SUBSCRIPTION
 * FIXED_ID_MESSAGE_SUBSCRIPTION        -> FIXED_ID_SUBSCRIPTION        -> ANY_SUBSCRIPTION
 * FIXED_ID_SERVICE_SUBSCRIPTION        -> FIXED_ID_SUBSCRIPTION        -> ANY_SUBSCRIPTION
 */

#define str(x) #x

#define defaults \
._sessions={},                                                                             \
._next = nullptr,                                                                          \
._port_id=0,


#define ANY_SUBSCRIPTION(_id, _type, _name, __extent, __kind, handler, timeout)            \
{                                                                                          \
.type=str(_type),                                                                          \
.name=_name,                                                                               \
.transfer_kind=__kind,                                                                     \
.subscription = {                                                                          \
.base=CanardTreeNode{},                                                                    \
.transfer_id_timeout_usec = timeout,                                                       \
.extent = __extent,                                                                        \
.port_id=_id,                                                                              \
.user_reference=(void *) handler,                                                          \
.sessions={}                                                                               \
}}

#define FIXED_ID_SUBSCRIPTION(nunavut_type, version_major, version_minor, handler, kind, sep, timeout) \
ANY_SUBSCRIPTION(                                                                               \
nunavut_type##_##version_major##_##version_minor##_FIXED_PORT_ID_,                              \
nunavut_type##sep##version_major##_##version_minor,                                             \
nunavut_type##_##version_major##_##version_minor##_FULL_NAME_,                                  \
nunavut_type##sep##version_major##_##version_minor##_EXTENT_BYTES_,                             \
kind,                                                                                           \
handler,                                                                                               \
timeout\
)

#define FIXED_ID_SERVICE_SUBSCRIPTION(nunavut_type, version_major, version_minor, handler, timeout) \
FIXED_ID_SUBSCRIPTION(nunavut_type, version_major, version_minor, handler,                 \
CanardTransferKindRequest, _Request_, timeout)

#define FIXED_ID_MESSAGE_SUBSCRIPTION(nunavut_type, version_major, version_minor, handler) \
FIXED_ID_SUBSCRIPTION(nunavut_type, version_major, version_minor, handler, CanardTransferKindMessage, _)


#define CONFIGURABLE_ID_SUBSCRIPTION(port_name, nunavut_type, version_major, version_minor, handler, kind, timeout)   \
ANY_SUBSCRIPTION(                                                                                            \
CONFIGURABLE_SUBJECT_ID,                                                                                     \
nunavut_type,                                                                                                \
str(uavcan.sub.port_name.id),                                                                                \
nunavut_type##_##version_major##_##version_minor##_EXTENT_BYTES_,                                            \
kind,                                                                                                        \
handler,                                                                                                     \
timeout                                                                                                      \
)

#define CONFIGURABLE_ID_SERVICE_SUBSCRIPTION(port_name, nunavut_type, version_major, version_minor, handler, timeout) \
CONFIGURABLE_ID_SUBSCRIPTION(port_name, nunavut_type, version_major, version_minor, handler, CanardTransferKindRequest, timeout)

#define CONFIGURABLE_ID_MESSAGE_SUBSCRIPTION(port_name, nunavut_type, version_major, version_minor, handler, timeout) \
CONFIGURABLE_ID_SUBSCRIPTION(port_name, nunavut_type, version_major, version_minor, handler, CanardTransferKindMessage, timeout)

