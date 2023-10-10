include(CMakeForceCompiler)
set(CMAKE_SYSTEM_NAME Generic)

set(CMAKE_CROSSCOMPILING 1)
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

SET(CMAKE_C_COMPILER_WORKS 1 CACHE INTERNAL "")
SET(CMAKE_CXX_COMPILER_WORKS 1 CACHE INTERNAL "")

set(TARGET "D:/gcc-arm-none-eabi-10.3-2021.10-win32/bin/")
set(CMAKE_C_COMPILER "${TARGET}arm-none-eabi-gcc.exe")
set(CMAKE_CXX_COMPILER "${TARGET}arm-none-eabi-g++.exe")
set(CMAKE_AR "${TARGET}arm-none-eabi-ar.exe")

set(CMAKE_C_FLAGS_INIT " -mcpu=cortex-m4 -fstack-protector-strong -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard \
-specs=nosys.specs -specs=nano.specs " CACHE STRING "c flags")

set(CMAKE_CXX_FLAGS_INIT " -mcpu=cortex-m4 -fstack-protector-strong -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard \
-specs=nosys.specs -specs=nano.specs " CACHE STRING "c++ flags")

set(__BIG_ENDIAN__ 0)