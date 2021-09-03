
#Requirements

* Be compatible with UAVCAN v1.0.
* Be compatible with UDRAL.
#Todo
1. For now postpone the integration of nunavut to this project and generate manually.
2. See https://github.com/UAVCAN/demos/blob/main/ds015_servo/src/main.c#L577
3. Implement register and heartbeat.
   1. Storage of configuration parameters using
      1. firmware/zubax_chibios/zubax_chibios/config/config.hpp
                This is an API for storing configuration on a configuration storage chip. 
      2. The actual configuration parameters are in an extensive list at the end of the https://files.zubax.com/products/io.px4.sapog/Sapog_v2_Reference_Manual.pdf. @7.2 Basic configuration
      3. Another really advanced option for storing configuration parameters would be https://github.com/littlefs-project/littlefs