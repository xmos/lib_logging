Using the logging library
=========================

Summary
-------

The logging library provides the ``debug_printf()`` function which is a lightweight
implementation of ``printf()``.  It also provides a framework for compile-time
control of which debug messages are enabled.

Software dependencies
.....................

For a list of direct dependencies, look for USED_MODULES in the Makefile.

Required hardware
.................

The example code provided with the application has been implemented
and tested on the xCORE-200 explorerKIT.

Prerequisites
..............

 * This document assumes familiarity with the XMOS xCORE architecture,
   the XMOS tool chain and the xC language. Documentation related to these
   aspects which are not specific to this application note are linked to in
   the references appendix.

 * For a description of XMOS related terms found in this document
   please see the XMOS Glossary [#]_.

.. [#] http://www.xmos.com/published/glossary

