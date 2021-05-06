#!/usr/bin/env python
# Copyright 2015-2021 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import xmostest

if __name__ == "__main__":
    xmostest.init()

    xmostest.register_group("lib_logging",
                            "simple_tests",
                            "Simple functionality tests",
    """
    There is currently just one test for this library. It is a simple test that
    uses the various format specifiers and checks the output.
    """)

    xmostest.runtests()

    xmostest.finish()
