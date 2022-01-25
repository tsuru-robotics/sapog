/// Copyright (c) 2016-2017  Zubax Robotics  <info@zubax.com>

#pragma once

#define _CHIBIOS_RT_CONF_
#define _CHIBIOS_RT_CONF_VER_5_0_

#define CH_CFG_INTERVALS_SIZE               32
#define CH_CFG_TIME_TYPES_SIZE              32

// High temporal granularity is required for the CAN driver; refer to that for more info.
// We can't use ticked mode for time tracking because the execution is stalled for a short time when we access flash.
// With tickless mode it is safe to use a very high timer frequency since there will be no CPU load penalties.
#define CH_CFG_ST_FREQUENCY                 100000
#define CH_CFG_ST_TIMEDELTA                 2
#define CH_CFG_ST_RESOLUTION                16

#define CH_CFG_TIME_QUANTUM                 0
#define CH_CFG_MEMCORE_SIZE                 0
#define CH_CFG_NO_IDLE_THREAD               FALSE

#define CH_CFG_OPTIMIZE_SPEED               FALSE

#define CH_CFG_USE_TM                       TRUE
#define CH_CFG_USE_REGISTRY                 FALSE
#define CH_CFG_USE_WAITEXIT                 FALSE
#define CH_CFG_USE_SEMAPHORES               FALSE
#define CH_CFG_USE_SEMAPHORES_PRIORITY      FALSE
#define CH_CFG_USE_MUTEXES                  TRUE
#define CH_CFG_USE_MUTEXES_RECURSIVE        CH_CFG_USE_MUTEXES
#define CH_CFG_USE_CONDVARS                 FALSE
#define CH_CFG_USE_CONDVARS_TIMEOUT         CH_CFG_USE_CONDVARS
#define CH_CFG_USE_EVENTS                   TRUE
#define CH_CFG_USE_EVENTS_TIMEOUT           CH_CFG_USE_EVENTS
#define CH_CFG_USE_MESSAGES                 FALSE
#define CH_CFG_USE_MESSAGES_PRIORITY        FALSE
#define CH_CFG_USE_MAILBOXES                FALSE
#define CH_CFG_USE_MEMCORE                  TRUE
#define CH_CFG_USE_HEAP                     TRUE
#define CH_CFG_USE_MEMPOOLS                 FALSE
#define CH_CFG_USE_DYNAMIC                  FALSE
#define CH_CFG_USE_OBJ_FIFOS                FALSE
#define CH_CFG_USE_FACTORY                  FALSE
#define CH_CFG_FACTORY_MAX_NAMES_LENGTH     FALSE
#define CH_CFG_FACTORY_OBJECTS_REGISTRY     FALSE
#define CH_CFG_FACTORY_GENERIC_BUFFERS      FALSE
#define CH_CFG_FACTORY_SEMAPHORES           FALSE
#define CH_CFG_FACTORY_MAILBOXES            FALSE
#define CH_CFG_FACTORY_OBJ_FIFOS            FALSE

#define CH_DBG_STATISTICS                   FALSE
#define CH_DBG_SYSTEM_STATE_CHECK           TRUE
#define CH_DBG_ENABLE_CHECKS                TRUE
#define CH_DBG_ENABLE_ASSERTS               TRUE
#define CH_DBG_ENABLE_STACK_CHECK           TRUE
#define CH_DBG_FILL_THREADS                 TRUE
#define CH_DBG_TRACE_MASK                   CH_DBG_TRACE_MASK_DISABLED
#define CH_DBG_TRACE_BUFFER_SIZE            128
#define CH_DBG_THREADS_PROFILING            FALSE

#define CH_CFG_THREAD_EXTRA_FIELDS
#define CH_CFG_SYSTEM_EXTRA_FIELDS

#define CH_CFG_SYSTEM_INIT_HOOK(tp)         { }

#define CH_CFG_THREAD_INIT_HOOK(tp)         { }
#define CH_CFG_THREAD_EXIT_HOOK(tp)         { }

#define CH_CFG_IRQ_PROLOGUE_HOOK()          { }
#define CH_CFG_IRQ_EPILOGUE_HOOK()          { }

#define CH_CFG_IDLE_ENTER_HOOK()            { }
#define CH_CFG_IDLE_LEAVE_HOOK()            { }
#define CH_CFG_IDLE_LOOP_HOOK()             { }

#define CH_CFG_TRACE_HOOK(tep)              { }

#define PORT_INT_REQUIRED_STACK             4096

#if !defined(__ASSEMBLER__) && !defined(__cplusplus)
extern void systemHaltHook(const char*);
#endif
#define CH_CFG_SYSTEM_HALT_HOOK(reason)     systemHaltHook(reason)

#define CH_CFG_CONTEXT_SWITCH_HOOK(...)     { }

#define CH_CFG_SYSTEM_TICK_HOOK()           { }