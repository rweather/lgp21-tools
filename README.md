LGP-21 Programming Tools
========================

This repository contains a set of tools in Python to help with
programming the LGP-21 computer.  It is based on the information
at [bitsavers](https://bitsavers.org/pdf/generalPrecision/LGP-21/).

## Dependencies

The Python tools use the "readchar" module to manage keyboard input,
so it is necessary to install that:

    pip install readchar

## A note on hexadecimal

The LGP-21 uses 0 to 9, f, g, j, k, q, and w as hexadecimal digits in
place of the usual 0 to 9 and A to F.  Lower case is preferred as the
digits 0 to 9 are also in the lower case version of the character set.

In tape images, words in hexadecimal are terminated with the
"conditional stop" character which is represented by a single quote:

    f02j8''800i0200'c0014'800i0200''u0008'

This corresponds to the following words:

    0x000A02C8      # f02j8'
    0x00000000      # '
    0x80040200      # 800i0200'
    0x000D0014      # c0014'
    0x80040200      # 800i0200'
    0x00000000      # '
    0x000A0008      # u0008'

You will note that the example above is using characters like i, c, and u
instead of "fgjkqw".  What gives?

It is still hexadecimal.  When the tape is loaded, the 6-bit character codes
are truncated to 4-bit and the i, c, and u characters magically end up having
the same bit-pattern as one of the standard hexadecimal characters:
i = 4, c = k, u = f.

It is common for LGP-21 program tapes to use non-standard hexadecimal
characters because they correspond to the instruction names: i = Input,
c = Clear, u = Unconditional Branch.  That makes it easier for humans to
prepare program tapes using the typewriter.

## Documentation

* [LGP-21 Programming Manual](https://bitsavers.org/pdf/generalPrecision/LGP-21/LGP-21_Programming_Manual_1963.pdf)
* [LGP-21 Reference Manual](https://bitsavers.org/pdf/generalPrecision/LGP-21/LGP-21_Reference_Manual_1963.pdf)
* [LGP-21 Coding Sheet](doc/LGP-21-Coding-Sheet.pdf)
* [Using the Program Input Routine](doc/pir-instructions.md)
* [Program Input Routine Bootstrap Process](doc/bootstrap.md)
* [Assembler Syntax Reference](doc/assembler-syntax.md)

## Converting tapes

The `lgp21-tape-to-ascii` tool converts binary .ptp tape images into
ASCII to make it easier to see what is on the tape.  The `lgp21-ascii-to-tape`
tool reverses the process:

    tools/lgp21-tape-to-ascii ascii.txt binary.ptp
    tools/lgp21-ascii-to-tape binary.ptp ascii.txt

Multiple input files can be concatenated to create a single output file:

    tools/lgp21-tape-to-ascii ascii.txt binary1.ptp binary2.ptp ...
    tools/lgp21-ascii-to-tape binary.ptp ascii1.txt ascii2.txt ...

The text conversion tools will expand or automatically insert upper/lower
case shift characters as necessary.  This may not work correctly if the tape
contains true binary data.  Paul Kimpel devised a binary-safe ASCII format
that avoids the problem.  To activate this, change the extension to "ptx":

    tools/lgp21-tape-to-ascii ascii.ptx binary.ptp
    tools/lgp21-ascii-to-tape binary.ptp ascii.ptx

Bitsavers has a collection of .ptp tape images in
[this directory](https://bitsavers.org/pdf/generalPrecision/LGP-21/paper_tapes/)
that can be used for testing.

## Running the emulator

A mini emulator written in Python is included.  No attempt has been made to
run this at the actual speed of the LGP-21.  It runs as fast as your host
machine can run.

    tools/lgp21-run

The emulator boostraps "Program Input Routine #2" into memory which is the
closest the LGP-21 has to an operating system from what I can tell.

After loading the "OS", the emulator will sit at the prompt waiting for a
command.  Characters can be typed in to effect commands.  But I currently
don't know what the commands are!  The LGP-21 uses the single-quote (')
character as a terminator but that's all I know.

Hit the ESC key to dump the entire contents of memory to stdout.  Press
CTRL-C to abort the emulator.

The emulator makes use of the Python tty and termios modules, which only
work on Unix/Linux systems.  Patches to make it work under non-POSIX
systems welcome.

The "-v" option to lgp21-run will dump the register values and
the current instruction as code is executed.

## License

Distributed under the terms of the MIT license.

## Contact

For more information on this code, to report bugs, or to suggest
improvements, please contact the author Rhys Weatherley via
[email](mailto:rhys.weatherley@gmail.com).
