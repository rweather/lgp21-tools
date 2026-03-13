LGP-21 Programming Tools
========================

This repository contains a set of tools in Python to help with
programming the LGP-21 computer.  It is based on the information
at [bitsavers](https://bitsavers.org/pdf/generalPrecision/LGP-21/).

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

## Converting tapes

The `lgp21-tape-to-ascii` tool converts binary .ptp tape images into
ASCII to make it easier to see what is on the tape.  The `lgp21-ascii-to-tape`
tool reverses the process:

    tools/lgp21-tape-to-ascii ascii.txt binary.ptp
    tools/lgp21-ascii-to-tape binary.ptp ascii.txt

Multiple input files can be concatenated to create a single output file:

    tools/lgp21-tape-to-ascii ascii.txt binary1.ptp binary2.ptp ...
    tools/lgp21-ascii-to-tape binary.ptp ascii1.txt ascii2.txt ...

Bitsavers has a collection of .ptp tape images in
[this directory](https://bitsavers.org/pdf/generalPrecision/LGP-21/paper_tapes/)
that can be used for testing.

## License

Distributed under the terms of the MIT license.

## Contact

For more information on this code, to report bugs, or to suggest
improvements, please contact the author Rhys Weatherley via
[email](mailto:rhys.weatherley@gmail.com).
