
This directory contains examples for the LGP-21 computer.  The examples
have the following files:

* `.asm` - Assembly source code.
* `.ptp` - Binary tape image for the main tape reader.
* `.hdr` - Header containg the bootstrap code for the `.ptp` image.
* `.txt` - Text version that can be pasted into the `lgp21-run` emulator.

Use the `.ptp` tape images when punching paper tapes to load into a
real LGP-21.  If a bootstrap is required, type the instructions in the
`.hdr` file into the computer with the tape loaded on the main tape reader.

The following assembly files are present:

* `1dlife.asm` - 1-D version of the Game of Life (tracks 15-17).
* `dump.asm` - Program that bootstraps into track 0 to dump the rest of the disk (track 0).
* `erase_disk.asm` - Program that lives in track 63 and erases the rest of the disk (track 63).
* `fibonacci.asm` - Prints a Fibonacci sequence in hexadecimal (track 12).
* `hellorld.asm` - Prints "he11or1d" to the typewriter (track 10).
* `print_strings.asm` - Example of printing terminated strings by address (track 11).
* `random.asm` - Library of routines to help generate random numbers.
* `rand_test.asm` - Test program for `random.asm`.
* `sier.asm` - Draws a Sierpiński Triangle fractal (tracks 13-14).
