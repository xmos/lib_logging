cmake_minimum_required(VERSION 3.21)
include($ENV{XMOS_CMAKE_PATH}/xcommon.cmake)
project(debug_printf_xc_test)

if(NOT DEFINED APP_HW_TARGET)
  set(APP_HW_TARGET XK-EVK-XU316)
endif()

set(APP_COMPILER_FLAGS -DDEBUG_PRINT_ENABLE=1)

include(${CMAKE_CURRENT_LIST_DIR}/../../examples/deps.cmake)
set(XMOS_SANDBOX_DIR ${CMAKE_CURRENT_LIST_DIR}/../../..)

XMOS_REGISTER_APP()
