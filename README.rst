:orphan:

###########################
lib_logging: Debug Printing
###########################

:vendor: XMOS
:version: 3.3.1
:scope: General Use
:description: Debug printing
:category: General Purpose
:keywords: logging, debugging
:devices: xcore.ai, xcore-200

********
Overview
********

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
Known Issues
************

  * None

**************
Required Tools
**************

  * XMOS XTC Tools: 15.3.0

*********************************
Required Libraries (dependencies)
*********************************

  * None

*************************
Related Application Notes
*************************

The following application notes use this library:

  * AN00239: Using the logging library

*******
Support
*******

This package is supported by XMOS Ltd. Issues can be raised against the software at: http://www.xmos.com/support
