:orphan:

###########################
lib_logging: Debug Printing
###########################

:vendor: XMOS
:version: 3.4.0
:scope: General Use
:description: Debug printing
:category: General Purpose
:keywords: logging, debugging
:devices: xcore.ai, xcore-200

*******
Summary
*******

This library provides a lightweight printf function that can be enabled
or disabled via configuration defines. Code can be declared to be
within a "debug unit" (usually a library or application source base)
and prints can be enabled/disabled per debug unit.

********
Features
********

* Low memory usage
* Ability to enable or disable printing via compile options
* Ability to enable or disable printing for sets of source files

************
Known issues
************

* None

****************
Development repo
****************

https://github.com/xmos/lib_logging

**************
Required tools
**************

* XMOS XTC Tools: 15.3.1

*********************************
Required libraries (dependencies)
*********************************

* None

*************************
Related application notes
*************************

* None

*******
Support
*******

This package is supported by XMOS Ltd. Issues can be raised against the software at: http://www.xmos.com/support
