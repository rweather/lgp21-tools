
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

# Fields within an instruction.
ORDER_MASK    = 0x800F0000  # Mask out the 5-bit order field.
ORDER_SHIFT   = 16          # LSB of the order field.
ADDRESS_MASK  = 0x00003FFC  # Mask out the 12-bit address field.
ADDRESS_SHIFT = 2           # LSB of the address field.
TRACK_MASK    = 0x00003F00  # Mask out the 6-bit track number field.
TRACK_SHIFT   = 8           # LSB of the track number field.
SECTOR_MASK   = 0x000000FC  # Mask out the 6-bit sector number field.
SECTOR_SHIFT  = 2           # LSB of the sector number field.

# Order codes.
STOP        = 0x00000000    # Stop ("Z")
OVERFLOW    = 0x80000000    # Sense overflow and transfer ("-Z")
BRING       = 0x00010000    # Bring value into accumulator ("B")
BRINGM      = 0x80010000    # Bring with the MSB set, same as "B".
STORE       = 0x00020000    # Store address at destination ("Y")
STOREM      = 0x80020000    # Store with the MSB set, same as "Y".
RETURN      = 0x00030000    # Set return address at destination ("R")
RETURNM     = 0x80030000    # Return with the MSB set, same as "R".
INPUT6      = 0x00040000    # Input or shift 6 bits ("I")
INPUT4      = 0x80040000    # Input or shift 4 bits ("-I")
DIV         = 0x00050000    # Division ("D")
DIVM        = 0x80050000    # Divide with the MSB set, same as "D".
MUL_L       = 0x00060000    # Multiply, return low bits of result ("N")
MUL_LM      = 0x80060000    # Multiply low with the MSB set, same as "N".
MUL_H       = 0x00070000    # Multiply, return high bits of result ("M")
MUL_HM      = 0x80070000    # Multiply high with the MSB set, same as "M".
PRINT6      = 0x00080000    # Print 6 bits ("P")
PRINT4      = 0x80080000    # Print 4 bits ("-P")
EXTRACT     = 0x00090000    # Extract / Bitwise AND ("E")
EXTRACTM    = 0x80090000    # Extract with the MSB set, same as "E".
UNCOND      = 0x000A0000    # Unconditional transfer ("U")
UNCONDM     = 0x800A0000    # Uncond jump with the MSB set, same as "U".
COND        = 0x000B0000    # Conditional transfer ("T")
CTRL        = 0x800B0000    # Transfer control ("-T")
HOLD        = 0x000C0000    # Store accumulator / hold in memory ("H")
HOLDM       = 0x800C0000    # Store accum with the MSB set, same as "H".
CLEAR       = 0x000D0000    # Store accumulator and clear ("C")
CLEARM      = 0x800D0000    # Clear with the MSB set, same as "C".
ADD         = 0x000E0000    # Addition ("A")
ADDM        = 0x800E0000    # Add with the MSB set, same as "A".
SUB         = 0x000F0000    # Subtraction ("S")
SUBM        = 0x800F0000    # Subtract with the MSB set, same as "S".

# Map order names to order codes.  Shown here as lower case as that is
# preferred when punching instructions to paper tape.
order_names = {
    STOP:       'z',
    OVERFLOW:   '-z',
    BRING:      'b',
    STORE:      'y',
    RETURN:     'r',
    INPUT6:     'i',
    INPUT4:     '-i',
    DIV:        'd',
    MUL_L:      'n',
    MUL_H:      'm',
    PRINT6:     'p',
    PRINT4:     '-p',
    EXTRACT:    'e',
    UNCOND:     'u',
    COND:       't',
    CTRL:       '-t',
    HOLD:       'h',
    CLEAR:      'c',
    ADD:        'a',
    SUB:        's'
}

# Map order codes to order names.
order_codes = {name: code for code, name in order_names.items()}

'''
Convert track/sector address into an operand address, shifted into the
correct place in an instruction word.
'''
def address(track, sector):
    global TRACK_MASK
    global TRACK_SHIFT
    global SECTOR_MASK
    global SECTOR_SHIFT
    return ((track << TRACK_SHIFT) & TRACK_MASK) | ((sector << SECTOR_SHIFT) & SECTOR_MASK)

'''
Extract the track portion of an operand address.
'''
def track(address):
    global TRACK_MASK
    global TRACK_SHIFT
    return (address & TRACK_MASK) >> TRACK_SHIFT

'''
Extract the sector portion of an operand address.
'''
def sector(address):
    global SECTOR_MASK
    global SECTOR_SHIFT
    return (address & SECTOR_MASK) >> SECTOR_SHIFT
