include(CMakeForceCompiler)
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR cortex-m4)

set(CMAKE_CROSSCOMPILING 1)
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

set(TARGET "D:/toolschain/gcc-arm-none-eabi-10-2020-q4-major-win32/bin/")
set(CMAKE_C_COMPILER "${TARGET}arm-none-eabi-gcc.exe")
set(CMAKE_CXX_COMPILER "${TARGET}arm-none-eabi-g++.exe")
set(CMAKE_AR "${TARGET}arm-none-eabi-ar.exe")

set(CMAKE_C_FLAGS_INIT " -mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard -ffunction-sections -fdata-sections -Dgcc -O0 -gdwarf-2 -g")
set(CMAKE_CXX_FLAGS_INIT " -mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard -ffunction-sections -fdata-sections -Dgcc -O0 -gdwarf-2 -g")


get_filename_component(script_path "${CMAKE_CURRENT_LIST_FILE}" ABSOLUTE)

string(REGEX MATCH "^(.*rt-thread)" RTT_ROOT_DIR "${script_path}")
string(REGEX MATCH "^(.*stm32f407-rt-spark)" BSP_ROOT_DIR "${script_path}")

include_directories(SYSTEM
${RTT_ROOT_DIR}/include              # kernel include
${RTT_ROOT_DIR}/components/finsh     # finsh include
${RTT_ROOT_DIR}/components/net/sal/include                      # #include <netdb.h>
${RTT_ROOT_DIR}/components/net/sal/include/socket               
${RTT_ROOT_DIR}/components/net/sal/include/socket/sys_socket    # #include <sys/socket.h>
${RTT_ROOT_DIR}/components/net/netdev/include
${RTT_ROOT_DIR}/components/net/netdev/include/arpa              # #include <arpa/inet.h>
${BSP_ROOT_DIR}                                                 # rtconfig.h
)

set(__BIG_ENDIAN__ 0)