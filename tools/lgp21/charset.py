
# Copyright (C) 2026 Rhys Weatherley
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# Maps 6-bit codes to their ASCII equivalents.
# Table III in Appendix C of the LGP-21 Programming Manual.
lowercase_chars = [
    '@',            # 0000 00 - Tape Feed, mapped to @
    'z',            # 0000 01 - z
    '0',            # 0000 10 - 0
    ' ',            # 0000 11 - Space
    chr(14),        # 0001 00 - Shift to lower case, mapped to Shift-Out (SO)
    'b',            # 0001 01 - b
    '1',            # 0001 10 - 1 or lower case L
    '-',            # 0001 11 - Minus
    chr(15),        # 0010 00 - Shift to upper case, mapped to Shift-In (SI)
    'y',            # 0010 01 - y
    '2',            # 0010 10 - 2
    '+',            # 0010 11 - +
    '^',            # 0011 00 - Color Shift, mapped to ^
    'r',            # 0011 01 - r
    '3',            # 0011 10 - 3
    ';',            # 0011 11 - ;
    '\n',           # 0100 00 - Carriage Return
    'i',            # 0100 01 - i
    '4',            # 0100 10 - 4
    '/',            # 0100 11 - /
    '\b',           # 0101 00 - Backspace
    'd',            # 0101 01 - d
    '5',            # 0101 10 - 5
    '.',            # 0101 11 - .
    '\t',           # 0110 00 - Tab
    'n',            # 0110 01 - n
    '6',            # 0110 10 - 6
    ',',            # 0110 11 - ,
    '',             # 0111 00 - Unused by typewriter
    'm',            # 0111 01 - m
    '7',            # 0111 10 - 7
    'v',            # 0111 11 - v
    "'",            # 1000 00 - Conditional stop, mapped to '
    'p',            # 1000 01 - p
    '8',            # 1000 10 - 8
    'o',            # 1000 11 - o
    '',             # 1001 00 - Unused by typewriter
    'e',            # 1001 01 - e
    '9',            # 1001 10 - 9
    'x',            # 1001 11 - x
    '',             # 1010 00 - Unused by typewriter
    'u',            # 1010 01 - u
    'f',            # 1010 10 - f
    '',             # 1010 11 - Unused by typewriter
    '',             # 1011 00 - Unused by typewriter
    't',            # 1011 01 - t
    'g',            # 1011 10 - g
    '',             # 1011 11 - Unused by typewriter
    '',             # 1100 00 - Unused by typewriter
    'h',            # 1100 01 - h
    'j',            # 1100 10 - j
    '',             # 1100 11 - Unused by typewriter
    '',             # 1101 00 - Unused by typewriter
    'c',            # 1101 01 - c
    'k',            # 1101 10 - k
    '',             # 1101 11 - Unused by typewriter
    '',             # 1110 00 - Unused by typewriter
    'a',            # 1110 01 - a
    'q',            # 1110 10 - q
    '',             # 1110 11 - Unused by typewriter
    '',             # 1111 00 - Unused by typewriter
    's',            # 1111 01 - s
    'w',            # 1111 10 - w
    '~'             # 1111 11 - Delete, mapped to ~
]
uppercase_chars = [
    '@',            # 0000 00 - Tape Feed, mapped to @
    'Z',            # 0000 01 - Z
    ')',            # 0000 10 - )
    ' ',            # 0000 11 - Space
    chr(14),        # 0001 00 - Shift to lower case, mapped to Shift-Out (SO)
    'B',            # 0001 01 - B
    'L',            # 0001 10 - L
    '_',            # 0001 11 - Underscore
    chr(15),        # 0010 00 - Shift to upper case, mapped to Shift-In (SI)
    'Y',            # 0010 01 - Y
    '*',            # 0010 10 - *
    '=',            # 0010 11 - =
    '^',            # 0011 00 - Color Shift, mapped to ^
    'R',            # 0011 01 - R
    '"',            # 0011 10 - "
    ':',            # 0011 11 - :
    '\n',           # 0100 00 - Carriage Return
    'I',            # 0100 01 - I
    '&',            # 0100 10 - Delta, mapped to &
    '?',            # 0100 11 - ?
    '\b',           # 0101 00 - Backspace
    'D',            # 0101 01 - D
    '%',            # 0101 10 - %
    ']',            # 0101 11 - ]
    '\t',           # 0110 00 - Tab
    'N',            # 0110 01 - N
    '$',            # 0110 10 - $
    '[',            # 0110 11 - [
    '',             # 0111 00 - Unused by typewriter
    'M',            # 0111 01 - M
    '#',            # 0111 10 - Pi, mapped to #
    'V',            # 0111 11 - V
    "'",            # 1000 00 - Conditional stop, mapped to '
    'P',            # 1000 01 - P
    '{',            # 1000 10 - Sigma, mapped to {
    'O',            # 1000 11 - O
    '',             # 1001 00 - Unused by typewriter
    'E',            # 1001 01 - E
    '(',            # 1001 10 - (
    'X',            # 1001 11 - X
    '',             # 1010 00 - Unused by typewriter
    'U',            # 1010 01 - U
    'F',            # 1010 10 - F
    '',             # 1010 11 - Unused by typewriter
    '',             # 1011 00 - Unused by typewriter
    'T',            # 1011 01 - T
    'G',            # 1011 10 - G
    '',             # 1011 11 - Unused by typewriter
    '',             # 1100 00 - Unused by typewriter
    'H',            # 1100 01 - H
    'J',            # 1100 10 - J
    '',             # 1100 11 - Unused by typewriter
    '',             # 1101 00 - Unused by typewriter
    'C',            # 1101 01 - C
    'K',            # 1101 10 - K
    '',             # 1101 11 - Unused by typewriter
    '',             # 1110 00 - Unused by typewriter
    'A',            # 1110 01 - A
    'Q',            # 1110 10 - Q
    '',             # 1110 11 - Unused by typewriter
    '',             # 1111 00 - Unused by typewriter
    'S',            # 1111 01 - S
    'W',            # 1111 10 - W
    '~'             # 1111 11 - Delete, mapped to ~
]

# Alternate encoding for binary tapes encoded in ASCII that
# preserves the original information as faithfully as possible.
# Format due to Paul Kimpel.
binary_chars = [
    '_',            # 0000 00 - Tape Feed, mapped to underscore
    'z',            # 0000 01 - z
    '0',            # 0000 10 - 0
    ' ',            # 0000 11 - Space
    '}',            # 0001 00 - Shift to lower case, mapped to }
    'b',            # 0001 01 - b
    '1',            # 0001 10 - 1 or lower case L
    '-',            # 0001 11 - Minus
    '{',            # 0010 00 - Shift to upper case, mapped to {
    'y',            # 0010 01 - y
    '2',            # 0010 10 - 2
    '+',            # 0010 11 - +
    '^',            # 0011 00 - Color Shift, mapped to ^
    'r',            # 0011 01 - r
    '3',            # 0011 10 - 3
    ';',            # 0011 11 - ;
    '<',            # 0100 00 - Carriage Return, mapped to <
    'i',            # 0100 01 - i
    '4',            # 0100 10 - 4
    '/',            # 0100 11 - /
    '!',            # 0101 00 - Backspace, mapped to !
    'd',            # 0101 01 - d
    '5',            # 0101 10 - 5
    '.',            # 0101 11 - .
    '|',            # 0110 00 - Tab, mapped to |
    'n',            # 0110 01 - n
    '6',            # 0110 10 - 6
    ',',            # 0110 11 - ,
    '"',            # 0111 00 - Unused by typewriter, mapped to "
    'm',            # 0111 01 - m
    '7',            # 0111 10 - 7
    'v',            # 0111 11 - v
    "'",            # 1000 00 - Conditional stop, mapped to '
    'p',            # 1000 01 - p
    '8',            # 1000 10 - 8
    'o',            # 1000 11 - o
    '$',            # 1001 00 - Unused by typewriter, mapped to $
    'e',            # 1001 01 - e
    '9',            # 1001 10 - 9
    'x',            # 1001 11 - x
    '%',            # 1010 00 - Unused by typewriter, mapped to %
    'u',            # 1010 01 - u
    'f',            # 1010 10 - f
    '=',            # 1010 11 - Unused by typewriter, mapped to =
    '&',            # 1011 00 - Unused by typewriter, mapped to &
    't',            # 1011 01 - t
    'g',            # 1011 10 - g
    '>',            # 1011 11 - Unused by typewriter, mapped to >
    '(',            # 1100 00 - Unused by typewriter, mapped to (
    'h',            # 1100 01 - h
    'j',            # 1100 10 - j
    '?',            # 1100 11 - Unused by typewriter, mapped to ?
    ')',            # 1101 00 - Unused by typewriter, mapped to )
    'c',            # 1101 01 - c
    'k',            # 1101 10 - k
    '@',            # 1101 11 - Unused by typewriter, mapped to @
    '*',            # 1110 00 - Unused by typewriter, mapped to *
    'a',            # 1110 01 - a
    'q',            # 1110 10 - q
    '`',            # 1110 11 - Unused by typewriter, mapped to back quote
    ':',            # 1111 00 - Unused by typewriter, mapped to colon
    's',            # 1111 01 - s
    'w',            # 1111 10 - w
    '~'             # 1111 11 - Delete, mapped to ~
]

'''
Converts a 6-bit I/O code into a 6-bit punch tape value.
'''
def io_6bit_to_punch(x):
    if type(x) is list:
        result = []
        for y in x:
            result.append(io_6bit_to_punch(y))
        return result
    return ((x & 0x3E) >> 1) | ((x & 0x01) << 5)

'''
Converts a 6-bit punch tape value into a 6-bit I/O code.
'''
def io_punch_to_6bit(x):
    return ((x & 0x20) >> 5) | ((x & 0x1F) << 1)

'''
Converts a 4-bit I/O code into a 6-bit I/O code.
'''
def io_4bit_to_6bit(x):
    return ((x & 0x0F) << 2) | 0x02

'''
Converts a 6-bit I/O code into a 4-bit I/O code.
'''
def io_6bit_to_4bit(x):
    return (x & 0x3C) >> 2

'''
Converts a 6-bit I/O code into an ASCII string.  May return an empty
string if there is no mapping to ASCII.

"upper" indicates if the upper case character set may be assumed to be
selected on entry.  Otherwise the lower case character set is selected.
'''
def io_6bit_to_ascii(x, upper=False):
    global lowercase_chars
    global uppercase_chars
    if type(x) is list:
        # Convert the entire list of 6-bit codes into a string
        # with processing for case shift characters.
        result = ''
        for code in x:
            if code == 0:
                # Reset back to lower case when we see a "Tape Feed" signal
                # which is used to separate sections on a tape.
                upper = False
            if upper:
                mapped = uppercase_chars[code & 0x3F]
            else:
                mapped = lowercase_chars[code & 0x3F]
            if mapped == chr(14):
                upper = False
            elif mapped == chr(15):
                upper = True
            else:
                result += mapped
        return result
    elif upper:
        return uppercase_chars[x & 0x3F]
    else:
        return lowercase_chars[x & 0x3F]

'''
Converts an ASCII character into a 6-bit I/O code.  Zero if not mapable.

"upper" indicates if the upper case character set may be assumed to be
selected on entry.  Otherwise the lower case character set is selected.

"force_shift" forces a shift code to be output at the start of the
result to select the case of the first character.

"as_list" forces the result to be a list of codes even if the string is
of length 0 or 1.  Otherwise strings of length 0 or 1 are mapped to a code.
'''
def io_ascii_to_6bit(x, upper=False, force_shift=False, as_list=False, end_in_lower=False):
    global lowercase_chars
    global uppercase_chars
    if len(x) == 0 and not as_list:
        # Empty strings map to Tape Feed / Zero.
        return 0
    elif len(x) == 1 and not as_list:
        # Convert a single-character string.
        if x == 'l':
            x = '1' # Special case for lower case L, which maps to 1.
        try:
            return uppercase_chars.index(x)
        except ValueError:
            try:
                return lowercase_chars.index(x)
            except ValueError:
                return 0
    else:
        # Convert a string into a list of 6-bit codes with
        # case shift codes inserted as necessary.
        result = []
        for c in x:
            # Special case for lower case L, which maps to 1.
            if c == 'l':
                ch = '1'
            else:
                ch = c

            # Try using the same case as the previous character.
            # Some characters are in both cases.
            if upper and not force_shift:
                try:
                    mapped = uppercase_chars.index(ch)
                    result.append(mapped)
                    continue
                except ValueError:
                    pass
            elif not upper and not force_shift:
                try:
                    mapped = lowercase_chars.index(ch)
                    result.append(mapped)
                    continue
                except ValueError:
                    pass

            # Shift to a different case from the previous character.
            force_shift = False
            try:
                mapped = lowercase_chars.index(ch)
                result.append(4) # Shift to lower case.
                result.append(mapped)
                upper = False
            except ValueError:
                try:
                    mapped = uppercase_chars.index(ch)
                    result.append(8) # Shift to upper case.
                    result.append(mapped)
                    upper = True
                except ValueError:
                    pass
        if end_in_lower and upper:
            # Force a shift to lower case at the end of the string.
            result.append(4)
        return result

'''
Converts a list of 6-bit I/O codes into the ASCII-ified binary ptx format.
'''
def io_6bit_to_ptx(x):
    global binary_chars
    result = ''
    for code in x:
        mapped = binary_chars[code & 0x3F]
        result += mapped
        if mapped == '<':
            # Newline is encoded as '<' but we can also put an
            # ignored newline afterwards to make it more readable.
            result += '\n'
    return result

'''
Converts an ASCII string into a list of 6-bit I/O codes using the
ASCII-ified binary ptx format.
'''
def io_ptx_to_6bit(x):
    global binary_chars
    result = []
    comment = False
    for c in x:
        # The encoding is case-insensitive; but "binary_chars" is not.
        ch = c.lower()

        # Handle out-of-band metadata comments that explain the tape
        # but are not part of it.  From '#' to the end of the line.
        if comment:
            if ch == '\n':
                comment = False
            continue
        elif ch == '#':
            comment = True
            continue

        # Map the character.  Unknown characters are treated as a comment.
        try:
            mapped = binary_chars.index(ch)
            result.append(mapped)
            continue
        except ValueError:
            pass
    return result
