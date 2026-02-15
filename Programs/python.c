/* Minimal main program -- everything is loaded from the library */

#include "Python.h"
#include <stdio.h>

#ifdef MS_WINDOWS
int
wmain(int argc, wchar_t **argv)
{
    return Py_Main(argc, argv);
}
#else
int
main(int argc, char **argv)
{
    /* Make stdio unbuffered early to avoid newlib __smakebuf_r crash.
       Without this, the first fprintf/fputc triggers buffer allocation
       via __smakebuf_r which crashes in the _malloc_r/_fstat_r chain.
       This also triggers __sinit(), initializing the FILE structs. */
    setvbuf(stdin,  NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    return Py_BytesMain(argc, argv);
}
#endif
