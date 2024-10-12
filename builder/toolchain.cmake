include(CMakeForceCompiler)
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR cortex-m4)

set(CMAKE_CROSSCOMPILING 1)
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

set(TARGET "C:/Program Files (x86)/GNU Arm Embedded Toolchain/10 2020-q4-major/bin/")
set(CMAKE_C_COMPILER "${TARGET}arm-none-eabi-gcc.exe")
set(CMAKE_CXX_COMPILER "${TARGET}arm-none-eabi-g++.exe")
set(CMAKE_AR "${TARGET}arm-none-eabi-ar.exe")

set(CMAKE_C_FLAGS_INIT " -mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard -ffunction-sections -fdata-sections -Dgcc -O0 -gdwarf-2 -g")
set(CMAKE_CXX_FLAGS_INIT " -mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard -ffunction-sections -fdata-sections -Dgcc -O0 -gdwarf-2 -g")

set(__BIG_ENDIAN__ 0)