// Copyright 2015-2021 XMOS LIMITED.
// This Software is subject to the terms of the XMOS Public Licence: Version 1.
#include <debug_print.h>

int main() {
  debug_printf("Hello World\n");
  debug_printf("An int: %d\n", -5);
  debug_printf("An unsigned int: %u\n", 5);
  debug_printf("A string: %s\n", "foo");
  debug_printf("A hexadecimal int: 0x%x\n", 0xabcd);
  debug_printf("A char: %c\n", 'X');

  return 0;
}