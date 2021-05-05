// Copyright 2015-2021 XMOS LIMITED.
// This Software is subject to the terms of the XMOS Public Licence: Version 1.
#include <debug_print.h>

int main() {
  debug_printf("Hello World\n");
  debug_printf("An int: %d\n", -5);
  debug_printf("An int: %D\n", -5);
  debug_printf("An unsigned int: %u\n", 5);
  debug_printf("An unsigned int: %U\n", 5);
  debug_printf("A string: %s\n", "foo");
  debug_printf("A string: %S\n", "FOO");
  debug_printf("A hexadecimal int: 0x%x\n", 0xabcd);
  debug_printf("A hexadecimal int: 0x%X\n", 0xabcd);
  debug_printf("A char: %c\n", 'x');
  debug_printf("A char: %C\n", 'X');

  int *p = 0;
  debug_printf("A pointer: %p\n", p);
  debug_printf("A pointer: %P\n", p);

  // Ignoring alignment and padding
  debug_printf("A hexadecimal int: 0x%08x\n", 0xabcd);
  debug_printf("A hexadecimal int: 0x%-10x\n", 0x1234);

  return 0;
}
