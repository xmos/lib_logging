set(LIB_NAME lib_logging)
set(LIB_VERSION 3.5.0)
set(LIB_INCLUDES api)
set(LIB_COMPILER_FLAGS  -Os
                        -Wall
                        -Wextra
                        -Wconversion
                        -Wdiv-by-zero
                        -Wfloat-equal
                        -Wsign-compare
                        -Werror)
set(LIB_DEPENDENT_MODULES "")
set(LIB_OPTIONAL_HEADERS debug_conf.h)

XMOS_REGISTER_MODULE()
