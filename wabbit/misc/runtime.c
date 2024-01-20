/* For LLVM, you need a runtime function to produce ouput.  Include
   this file with final compilation with clang. For example:

   shell % clang out.ll misc/runtime.c -o out.exe
*/

#include <stdio.h>
#include <stdbool.h>

int _print_int(int x) {
  printf("%i\n", x);
  return 0;
}

int _print_float(double x) {
    printf("%lf\n", x);
    return 0;
}

int _print_char(int c) {
    printf("%c", c);
    return 0;
}

int _print_bool(bool b) {
    printf("%s\n", b ? "true" : "false");
    return 0;
}