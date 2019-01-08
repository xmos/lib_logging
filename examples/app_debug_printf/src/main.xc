// Copyright (c) 2015-2019, XMOS Ltd, All rights reserved
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