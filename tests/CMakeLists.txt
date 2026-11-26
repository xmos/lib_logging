cmake_minimum_required(VERSION 3.21)
include($ENV{XMOS_CMAKE_PATH}/xcommon.cmake)
project(tests)

# XC sources require the XS/XTC 15 toolchain and cannot be built for VX targets.
option(LOGGING_BUILD_XC_TESTS "Build XS-only XC compatibility tests" OFF)

add_subdirectory(debug_printf_test)

if(LOGGING_BUILD_XC_TESTS)
  add_subdirectory(debug_printf_xc_test)
endif()
