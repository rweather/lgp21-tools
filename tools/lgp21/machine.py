
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

import lgp21.charset as charset
import lgp21.insn as insn

# Contents of the Program Input Routine #2 tape.
# https://bitsavers.org/pdf/generalPrecision/LGP-21/paper_tapes/Program_Input_%232.ptp
Program_Input_Routine = """000c0018'u0008'c3w00'800i0000'c3w04'gwc0000'c3w08'
u3w20'c3w20'b3w04'c3w24's3w44'c3w28't3w34'
c3w2j'c3w04'c3w30'u3w00'c3w34''c3w38'u0000'
c3w44'wwwwj'u3w00''
f02j8''800i0200'c0014'800i0200''u0008'
200fj'20194'201fj'k0104'q00w4'f0048'wj00'10000'wwwwwwj''
100w4'k00w4'80040000'j0118'q0074'80000200'f0208'600g8'j0110'90230'
70078'f0080'10000000'k0000000'k3wwj'q0110'j0114'90034'70264'f00f0'
q00g4'g0174'f02k4'q0114'20118'f00gj''70100000'20040000'4'1024j'
90118'q0170'80000200'f0094'6016j'g029j'10268'q0118'f00w0'10060004'
f0150'ww30000'90248''1026j'f002j'k0120'40000'f019j'2000''''''2'
80000200'f0130'k0114'80040000'w011j'g0148'w0124'g0048'k0110'800g004j'
10204'80200'43w00'80200'80200'2'f02k0'100'70000000'q003j'g0270'
601gj'q00w4'k01f4'10118'g0100'k0120'80040000'f01f4'6026j'j0114''f01j0'''
'f004j'40000'101f4'q0200'g01k0'f0184'9007j'k00w4'f01kj'
10118'g01q8'f0044'101f4'k01g4'10164'q0114'f01g4'ww60000'www00004'
94k00000'w0228'j011j'w00g0'j0234'q0038'k023j'80040000'f0234'10000000''
3j3j0''1011j''k011j'f0250'800w3wwj'709w3wwj'10234'q0200'g0128'f0214'
40200'f0000000''4'q00q4'g0288'j0110'k0118'k0114'f010j'q01wj'g02f4'
k0268'f004j''k0110'f00kj'q02j4'g02g0'f0048'q00qj't02q8'k0040'
80040000'f0040'100k0000'100q8'k00w4'10260'202gj'2004j'20134'20220'f0020'
202qj'10000''102qj'q026j'f02q8'
"""

'''
Converts a 32-bit word into its signed 31-bit form.
'''
def to_signed(value):
    # Lose the LSB as that is an unused "spacer" bit in the LGP-21.
    value = value >> 1

    # Negate the value if the sign bit is set.
    if (value & 0x40000000) != 0:
        value = (value ^ 0x7FFFFFFF) + 1
        return -value
    else:
        return value

'''
Converts the signed 31-bit form of a word back into a 32-bit word.
Returns the 32-bit form and the overflow indicator.
'''
def from_signed(value):
    if value < -0x40000000 or value > 0x3FFFFFFF:
        overflow = True
    else:
        overflow = False
    if value < 0:
        value = -value
        value = (value ^ 0x7FFFFFFF) + 1
    return ((value << 1) & 0xFFFFFFFE, overflow)

'''
Multiply two words and return the low or high part of the 62-bit result.
'''
def multiply(x, y, high):
    value = to_signed(x) * to_signed(y)
    if value < 0:
        value = -value
        value = (value ^ 0x3FFFFFFFFFFFFFFF) + 1
    if high:
        return (value >> 30) & 0xFFFFFFFE
    else:
        return (value << 1) & 0xFFFFFFFE

'''
Divide x by y and return the quotient rounded to 30 bits.

Note: The values are interpreted as fractions -1.0 <= value < 1.0
so this isn't straight integer division.
'''
def divide(x, y):
    xval = to_signed(x)
    yval = to_signed(y)
    if xval < 0 and yval < 0:
        xval = -xval
        yval = -yval
        sign = False
    elif xval < 0:
        xval = -xval
        sign = True
    elif yval < 0:
        yval = -yval
        sign = True
    else:
        sign = False
    if y == 0:
        # Division by zero produces an all-1's value and overflow.
        # Is this correct?  Should the machine catch on fire instead?
        return (0xFFFFFFFE, True)
    result = int((x << 31) / y) + 1
    result = result >> 1 # Account for the extra rounding bit.
    if sign:
        result = -result
    return from_signed(result)

'''
LGP-21 machine execution engine.
'''
class Machine:
    '''
    Initialize the machine.
    '''
    def __init__(self):
        self.memory = [0] * 4096
        self.A = 0
        self.C = 0
        self.overflow = False
        self.halted = True
        self.TC = False # State of the TC switch on the console.
        self.BS = 0     # State of the branch switches on the console.
        self.tape = []

    '''
    Bootstraps the machine and loads the program input routine
    on the tape reader.
    '''
    def bootstrap(self):
        global Program_Input_Routine

        # Preload the 3-word bootstrap and prepare to execute it.
        # Normally this is bootstraped by hand using the front panel.
        # We skip ahead to the point where the bootstrap is loaded.
        self.memory[2] = 0x80040000 # Input a word from the tape reader into A.
        self.memory[3] = 0x000D0014 # Store to address 5 and clear A.
        self.memory[4] = 0x80040000 # Input a word from the tape reader into A.
        self.A = 0                  # Clear the accumulator.
        self.C = 2                  # Set the initial program counter to 2.
        self.overflow = False       # Clear the overflow bit.
        self.halted = False         # Take the machine out of the halt state.

        # Load the program input routine up on the tape reader.
        self.tape = charset.io_ascii_to_6bit(Program_Input_Routine)

    '''
    Halt the machine.
    '''
    def halt(self):
        self.halted = True

    '''
    Resume execution after a halt.
    '''
    def resume(self):
        self.halted = False

    '''
    Determine if the machine is currently halted.
    '''
    def is_halted(self):
        return self.halted

    '''
    Perform a single instruction step.
    '''
    def step(self):
        # Fetch the next instruction and increment the program counter.
        inst = self.memory[self.C]
        self.C = (self.C + 1) & 4095

        # Break the instruction up into its constituent parts.
        opcode = inst & insn.ORDER_MASK
        address = (inst & insn.ADDRESS_MASK) >> insn.ADDRESS_SHIFT
        track = address >> 6

        # Determine what needs to be done.
        match opcode:
            case insn.STOP:
                # Z: Conditional stop of the machine.
                if track == 0 or track == 1:
                    # Z0000 or Z0100 halt the machine.
                    self.halted = True
                elif track == 2 or track == 0x00C03:
                    # Z0200 or Z0300 are no-op instructions.
                    pass
                elif (track & self.BS) != track:
                    # Skip the next instruction based on the branch switches.
                    self.C = (self.C + 1) & 4095

            case insn.OVERFLOW:
                # -Z: Sense overflow and transfer.
                skip = False
                if track == 0 or track == 1:
                    # -Z0000 or -Z0100 halt the machine and optionally skip.
                    if self.overflow:
                        self.overflow = False
                        skip = True
                    self.halted = True
                elif track == 2 or track == 3:
                    # -Z0200 or -Z0300 skip based on overflow only.
                    if self.overflow:
                        self.overflow = False
                        skip = True
                elif self.overflow or (track & self.BS) != track:
                    # Skip based on overflow or the branch switches.
                    self.overflow = False
                    skip = True
                if skip:
                    self.C = (self.C + 1) & 4095

            case insn.BRING:
                # B: Bring a value into the accumulator from memory.
                self.A = self.memory[address]

            case insn.STORE:
                # Y: Store to the address field only at the destination.
                temp = self.memory[address] & ~insn.ADDRESS_MASK
                self.memory[address] = temp | (self.A & insn.ADDRESS_MASK)

            case insn.RETURN:
                # T: Store the return address at the destination.
                temp = self.memory[address] & ~insn.ADDRESS_MASK
                temp2 = ((self.C + 1) & 4095) << insn.ADDRESS_SHIFT
                self.memory[address] = temp | temp2

            case insn.INPUT6:
                # TODO
                pass

            case insn.INPUT4:
                # TODO
                pass

            case insn.DIV:
                # D: Divide the value in the accumulator by a value in memory.
                self.A, overflow = divide(self.A, self.memory[address])

            case insn.MUL_L:
                # N: Multiply memory with accumulator, return low word.
                self.A = multiply(self.A, self.memory[address], False)

            case insn.MUL_H:
                # M: Multiply memory with accumulator, return high word.
                self.A = multiply(self.A, self.memory[address], True)

            case insn.PRINT6:
                # TODO
                pass

            case insn.PRINT4:
                # TODO
                pass

            case insn.EXTRACT:
                # E: Extract bits / bitwise AND.
                self.A = self.A & self.memory[address]

            case insn.UNCOND:
                # U: Unconditional branch.
                self.C = address

            case insn.COND:
                # T: Conditional branch if the sign bit of A is set.
                if (self.A & 0x80000000) != 0:
                    self.C = address

            case insn.CTRL:
                # -T: Conditional branch if the sign bit of A is set,
                # or if the TC switch is set on the console.
                if (self.A & 0x80000000) != 0 or self.TC:
                    self.C = address

            case insn.HOLD:
                # H: Hold / store the accumulator to memory.
                # Memory is 31-bit not 32-bit, so drop the LSB.
                self.memory[address] = self.A & 0xFFFFFFFE

            case insn.CLEAR:
                # C: Store the accumulator to memory and then clear.
                self.memory[address] = self.A & 0xFFFFFFFE
                self.A = 0

            case insn.ADD:
                # A: Add the contents of memory to the accumulator.
                self.A, overflow = from_signed(to_signed(self.A) + to_signed(self.memory[address]))

            case insn.SUB:
                # S: Subtract the contents of memory from the accumulator.
                self.A, overflow = from_signed(to_signed(self.A) - to_signed(self.memory[address]))

            case _:
                # Unknown instruction.  Treat it as a no-op for now.
                pass

    '''
    Run the machine continuously until it halts.  Does nothing if the
    machine is already halted.
    '''
    def run(self):
        while not self.halted:
            self.step()
