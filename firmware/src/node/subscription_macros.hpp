#pragma once

#include "libcanard/canard.h"

#define str(x) #x

#define defaults \
._sessions={},                                                                             \
._next = nullptr,                                                                          \
._port_id=0,


#define ANY_SUBSCRIPTION(_id, _type, _name, __extent, __kind, handler)                     \
{                                                                                          \
.type=str(_type),                                                                          \
.name=_name,                                                                               \
.transfer_kind=__kind,                                                                     \
.subscription = {                                                                          \
._next = nullptr,                                                                          \
._sessions={},                                                                             \
._transfer_id_timeout_usec = CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC,                      \
._extent = __extent,                                                                       \
._port_id=_id,                                                                             \
.user_reference=(void *) handler                                                           \
}}

#define FIXED_ID_SUBSCRIPTION(nunavut_type, version_major, version_minor, handler, kind, sep)   \
ANY_SUBSCRIPTION(                                                                               \
nunavut_type##_##version_major##_##version_minor##_FIXED_PORT_ID_,                              \
nunavut_type##sep##version_major##_##version_minor,                                             \
nunavut_type##_##version_major##_##version_minor##_FULL_NAME_,                                  \
nunavut_type##sep##version_major##_##version_minor##_EXTENT_BYTES_,                             \
kind,                                                                                           \
handler                                                                                         \
)

#define FIXED_ID_SERVICE_SUBSCRIPTION(nunavut_type, version_major, version_minor, handler) \
FIXED_ID_SUBSCRIPTION(nunavut_type, version_major, version_minor, handler,                 \
CanardTransferKindRequest, _Request_)

#define FIXED_ID_MESSAGE_SUBSCRIPTION(nunavut_type, version_major, version_minor, handler) \
FIXED_ID_SUBSCRIPTION(nunavut_type, version_major, version_minor, handler, CanardTransferKindMessage, _)


#define CONFIGURABLE_ID_SUBSCRIPTION(port_name, nunavut_type, version_major, version_minor, handler, kind)   \
ANY_SUBSCRIPTION(                                                                                            \
CONFIGURABLE_SUBJECT_ID,                                                                                     \
nunavut_type,                                                                                                \
str(uavcan.sub.port_name.id),                                                                                \
nunavut_type##_##version_major##_##version_minor##_EXTENT_BYTES_,                                            \
kind,                                                                                                        \
handler                                                                                                      \
)

#define CONFIGURABLE_ID_SERVICE_SUBSCRIPTION(port_name, nunavut_type, version_major, version_minor, handler) \
CONFIGURABLE_ID_SUBSCRIPTION(port_name, nunavut_type, version_major, version_minor, handler, CanardTransferKindRequest)

#define CONFIGURABLE_ID_MESSAGE_SUBSCRIPTION(port_name, nunavut_type, version_major, version_minor, handler) \
CONFIGURABLE_ID_SUBSCRIPTION(port_name, nunavut_type, version_major, version_minor, handler, CanardTransferKindMessage)

