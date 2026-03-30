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

import lgp21.insn as insn

# Sector numbering sequence from chapter 8 of the LGP-21 programming manual.
optimum_address_locator = [
    0, 64, 57, 121, 50, 114, 43, 107, 36, 100, 29, 93, 22, 86, 15, 79, 8,  72,
    1, 65, 58, 122, 51, 115, 44, 108, 37, 101, 30, 94, 23, 87, 16, 80, 9,  73,
    2, 66, 59, 123, 52, 116, 45, 109, 38, 102, 31, 95, 24, 88, 17, 81, 10, 74,
    3, 67, 60, 124, 53, 117, 46, 110, 39, 103, 32, 96, 25, 89, 18, 82, 11, 75,
    4, 68, 61, 125, 54, 118, 47, 111, 40, 104, 33, 97, 26, 90, 19, 83, 12, 76,
    5, 69, 62, 126, 55, 119, 48, 112, 41, 105, 34, 98, 27, 91, 20, 84, 13, 77,
    6, 70, 63, 127, 56, 120, 49, 113, 42, 106, 35, 99, 28, 92, 21, 85, 14, 78, 7, 71
]

'''
Get the next rotational disk location after "loc"; e.g. 64 is after 0.

If "advance" is greater than zero, advance that many locations.
'''
def next_disk_location(loc, advance=1):
    global optimum_address_locator
    pos=optimum_address_locator.index(loc&127)
    while advance >= 1:
        pos = (pos + 1) & 127
        advance -= 1
    return optimum_address_locator[pos]

'''
Get the number of word times for moving from a source address to a
destination address on the disk.
'''
def word_times_for_addressing(src, dest):
    global optimum_address_locator

    # Find the starting position.
    posn = optimum_address_locator.index(src & 127)
    poscount = 0
    # Scan forward until we find the destination.
    while optimum_address_locator[posn] != (dest & 127):
        posn = (posn + 1) & 127
        poscount += 1
    # Determine the number of word times, accounting for circular rotation.
    # If the source and destination were the same, this will cause a
    # complete disk rotation to happen to get to the destination.
    return poscount

'''
Get the number of word times for executing a specific instruction
that was loaded from "PC".

"disk_loc" is the rotational position on the magnetic disk before the
instruction fetch; between 0 and 127.

Returns (time, disk_loc) for the number of word times and the new
rotational disk location after the instruction finishes executing.
'''
def word_times_for_insn(disk_loc, PC, word):
    # Phase 1: Seek forward to find the PC if we were not lucky
    # enough to have it already underneath the read head.
    if disk_loc != (PC & 127):
        time = word_times_for_addressing(disk_loc, PC)
    else:
        time = 0
    disk_loc = PC & 127

    # Phase 2: One word time for the instruction fetch.
    time += 1
    disk_loc = next_disk_location(disk_loc)

    # Phase 3 and 4: Depends upon the type of instruction.
    addr = (word & insn.ADDRESS_MASK) >> insn.ADDRESS_SHIFT
    match word & insn.ORDER_MASK:
        case insn.STOP | insn.OVERFLOW:
            # These instructions are always optimum.  If a branch is taken
            # due to switch sensing, the caller will account for that.
            pass

        case insn.BRING | insn.BRINGM | insn.STORE | insn.STOREM | insn.RETURN | insn.RETURNM | insn.EXTRACT | insn.EXTRACTM | insn.HOLD | insn.HOLDM | insn.CLEAR | insn.CLEARM | insn.ADD | insn.ADDM | insn.SUB | insn.SUBM:
            # Phase 3: Seek forward to find the memory operand.
            if (addr & 127) != disk_loc:
                time += word_times_for_addressing(disk_loc, addr)
                disk_loc = addr & 127

            # Phase 4: One extra word time to perform the instruction.
            time += 1
            disk_loc = next_disk_location(disk_loc)

        case insn.INPUT6 | insn.INPUT4:
            # Input blocks the computer, so the timing is unknowable.
            # Shift operations will be near-optimum with 1 word time.
            time += 1
            disk_loc = next_disk_location(disk_loc)

        case insn.DIV | insn.DIVM:
            # Phase 3: Seek forward to find the memory operand.
            if (addr & 127) != disk_loc:
                time += word_times_for_addressing(disk_loc, addr)
                disk_loc = addr & 127

            # Phase 4: 66 word times to perform the division.
            time += 66
            disk_loc = next_disk_location(disk_loc, advance=66)

        case insn.MUL_L | insn.MUL_LM:
            # Phase 3: Seek forward to find the memory operand.
            if (addr & 127) != disk_loc:
                time += word_times_for_addressing(disk_loc, addr)
                disk_loc = addr & 127

            # Phase 4: 63 word times to perform the low multiplication.
            time += 63
            disk_loc = next_disk_location(disk_loc, advance=63)

        case insn.MUL_H | insn.MUL_HM:
            # Phase 3: Seek forward to find the memory operand.
            if (addr & 127) != disk_loc:
                time += word_times_for_addressing(disk_loc, addr)
                disk_loc = addr & 127

            # Phase 4: 65 word times to perform the high multiplication.
            time += 65
            disk_loc = next_disk_location(disk_loc, advance=65)

        case insn.PRINT6 | insn.PRINT4:
            # Printing to the tape punch is ~1/3 revolutions and printing
            # to the typewriter is ~2 revolutions.  The actual hardware
            # uses lookahead, so it is possible to run instructions in the
            # time between prints.  This is hard to account for, so we
            # instead act as though printing is blocking.
            device = (word & insn.TRACK_MASK) >> insn.TRACK_SHIFT
            if device == 2:
                num_words = 256
            else:
                num_words = 43
            time += num_words
            disk_loc = next_disk_location(disk_loc, advance=num_words)

        case insn.UNCOND | insn.UNCONDM | insn.COND | insn.CTRL:
            # Branch instructions are at least 4 word times, plus the
            # time to find the PC if the branch is taken.  The caller
            # will deal with taken branches.
            time += 2
            disk_loc = next_disk_location(disk_loc, advance=2)

    # Done!
    return (time, disk_loc)
