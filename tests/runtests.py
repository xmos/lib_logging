#!/usr/bin/env python
import xmostest

xmostest.init()

xmostest.register_group("lib_logging",
                        "simple_tests",
                        "Simple functionality tests",
"""
There is currently just one test for this library. It is a simple test that
uses the various format specifiers and checks the output.
""")

resources = xmostest.request_resource("xsim")

tester = xmostest.ComparisonTester(open('test.expect'),
                                   'lib_logging', 'simple_tests',
                                   'basic_functionality_test', {})

xmostest.run_on_simulator(resources['xsim'],
                          'debug_printf_test/bin/debug_printf_test.xe',
                          tester=tester)

xmostest.finish()
