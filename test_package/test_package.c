#include <stdio.h>
#include <stdlib.h>

#include "dyncall.h"

static int
plusone(int n)
{
    return n + 1;
}

int
main(int argc, char *argv[])
{
    int n;

    DCCallVM* vm = dcNewCallVM(4096);
    dcMode(vm, DC_CALL_C_DEFAULT);
    dcReset(vm);
    dcArgInt(vm, 1);
    n = dcCallInt(vm, (DCpointer)&plusone);
    dcFree(vm);

    return n == 2 ? EXIT_SUCCESS : EXIT_FAILURE;
}
