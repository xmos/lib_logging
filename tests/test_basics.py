# Copyright 2018-2021 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import xmostest

def runtest():
    resources = xmostest.request_resource("xsim")

    tester = xmostest.ComparisonTester(open('test.expect'),
                                       'lib_logging', 'simple_tests',
                                       'basic_functionality_test', {})

    xmostest.run_on_simulator(resources['xsim'],
                              'debug_printf_test/bin/debug_printf_test.xe',
                              tester=tester)
