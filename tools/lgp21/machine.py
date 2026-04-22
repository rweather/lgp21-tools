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

import readchar
import random
import lgp21.charset as charset
import lgp21.dis as dis
import lgp21.hexadecimal as hexadecimal
import lgp21.insn as insn
import lgp21.timing as timing
import sys

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
Converts a 32-bit word into its signed form.
'''
def to_signed(value):
    if (value & 0x80000000) != 0:
        value = (value ^ 0xFFFFFFFF) + 1
        return -value
    else:
        return value

'''
Converts the signed form of a word back into a 32-bit word.
Returns the 32-bit form and the overflow indicator.
'''
def from_signed(value):
    if value < -0x80000000 or value > 0x7FFFFFFF:
        overflow = True
    else:
        overflow = False
    if value < 0:
        value = -value
        value = (value ^ 0xFFFFFFFF) + 1
    return (value & 0xFFFFFFFF, overflow)

'''
Add two 32-bit words, returning the value and the overflow indicator.
'''
def add(x, y):
    return from_signed(to_signed(x) + to_signed(y))

'''
Subtract two 32-bit words, returning the value and the overflow indicator.
'''
def sub(x, y):
    return from_signed(to_signed(x) - to_signed(y))

'''
Multiply two words and return the low or high part of the 62-bit result.
'''
def multiply(x, y, high):
    value = to_signed(x) * to_signed(y)
    if value < 0:
        value = -value
        value = (value ^ 0xFFFFFFFFFFFFFFFF) + 1
    if high:
        return (value >> 31) & 0xFFFFFFFE
    else:
        return value & 0xFFFFFFFE

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
    if yval == 0:
        # Division by zero produces an all-1's value and overflow.
        # Is this correct?  Should the machine catch on fire instead?
        return (0xFFFFFFFF, True)
    result = int((xval << 32) / yval) + 1
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
        self.tape_posn = 0
        self.pre_typed_input = []
        self.print_upper = False
        self.print_color = False
        self.input_upper = False
        self.input_buffer = -1
        self.loading_bootstrap = False
        self.verbose = False
        self.word_times = 0
        self.disk_loc = 0

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
        self.print_upper = False    # Reset the state of the typewriter.
        self.input_upper = False
        self.input_buffer = -1
        self.loading_bootstrap = True

        # Load the program input routine up on the tape reader.
        self.tape = charset.io_ascii_to_6bit(Program_Input_Routine)
        self.tape_posn = 0

    '''
    Bootstraps the machine from an external tape, bypassing the PIR.

    It is assumed that the tape is for the typewriter, not the tape reader.
    '''
    def bootstrap_from_tape(self, filename, binary=False, raw_data=''):
        # Read the contents of the tape into memory.
        if len(raw_data) > 0:
            self.pre_typed_input = self.pre_typed_input + charset.io_ascii_to_6bit(raw_data, as_list=True, end_in_lower=True)
        elif binary:
            with open(filename, 'rb') as file:
                for b in file.read():
                    self.pre_typed_input.append(charset.io_punch_to_6bit(int(b)))
        else:
            with open(filename, 'r') as file:
                self.pre_typed_input = self.pre_typed_input + charset.io_ascii_to_6bit(file.read(), as_list=True, end_in_lower=True)

        # Read pairs of words for the instruction and data to execute.
        # Stop once we see a jump instruction, as that indicates that the
        # manual portion of the bootstrap process has completed.
        while True:
            self._input(2, 4)
            inst = self.A
            self._input(2, 4)
            if (inst & insn.ORDER_MASK) == insn.UNCOND:
                # We have reached the unconditional jump in the bootstrap.
                self.C = (inst & insn.ADDRESS_MASK) >> insn.ADDRESS_SHIFT
                break
            if (inst & insn.ORDER_MASK) != insn.CLEAR:
                # The only regular instruction we accept is "c".
                return False
            self.memory[(inst & insn.ADDRESS_MASK) >> insn.ADDRESS_SHIFT] = self.A
            self.A = 0

        # Take the machine out of halt to prepare to execute the bootstrap.
        self.halted = False
        return True

    '''
    Set up to load a tape after the current one is exhausted.

    If a previous tape was already loaded, this will append the contents
    of the new tape.
    '''
    def load_tape(self, filename, binary=False):
        if binary:
            with open(filename, 'rb') as file:
                for b in file.read():
                    self.pre_typed_input.append(charset.io_punch_to_6bit(int(b)))
        else:
            with open(filename, 'r') as file:
                self.pre_typed_input = self.pre_typed_input + charset.io_ascii_to_6bit(file.read(), as_list=True, end_in_lower=True)

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
        # Fetch the next instruction, account for instruction timings, and
        # increment the program counter.
        iaddr = self.C
        inst = self.memory[self.C]
        time, self.disk_loc = timing.word_times_for_insn(self.disk_loc, self.C, inst)
        self.word_times += time
        self.C = (self.C + 1) & 4095

        # Break the instruction up into its constituent parts.
        opcode = inst & insn.ORDER_MASK
        address = (inst & insn.ADDRESS_MASK) >> insn.ADDRESS_SHIFT
        track = address >> 6

        # Print the instruction - for debugging.
        if self.verbose:
            inststr = hexadecimal.to_hex(inst, min_digits=1, order_codes=True)
            print("A = %08x, overflow = %d" % (self.A, int(self.overflow)))
            print("%02d%02d  %8s'  %s" % (iaddr / 64, iaddr % 64, inststr, dis.disassemble(inst)))

        # Determine what needs to be done.
        match opcode:
            case insn.STOP:
                # Z: Conditional stop of the machine.
                if track == 0 or track == 1:
                    # Z0000 or Z0100 halt the machine.  If we were
                    # bootstrapping the system, switch to running the
                    # Program Input Routine that is now in memory.
                    if self.loading_bootstrap:
                        self.loading_bootstrap = False
                        self.A = 0
                        self.C = 0
                    else:
                        self.halted = True
                elif track == 2 or track == 3:
                    # Z0200 or Z0300 are no-op instructions.
                    # Z0300 has been repurposed to print accumulated timing.
                    if track == 3:
                        self.print_time()
                elif (track & self.BS) != track:
                    # Skip the next instruction based on the branch switches.
                    self.C = (self.C + 1) & 4095

            case insn.OVERFLOW:
                # -Z: Sense overflow and transfer.
                skip = False
                if track == 0 or track == 1:
                    # -Z0000 or -Z0100 halt the machine and optionally skip.
                    if not self.overflow:
                        skip = True
                    self.halted = True
                elif track == 2 or track == 3:
                    # -Z0200 or -Z0300 skip based on overflow only.
                    if not self.overflow:
                        skip = True
                elif (not self.overflow) or (track & self.BS) != track:
                    # Skip based on overflow or the branch switches.
                    skip = True
                self.overflow = False
                if skip:
                    self.C = (self.C + 1) & 4095

            case insn.BRING | insn.BRINGM:
                # B: Bring a value into the accumulator from memory.
                self.A = self.memory[address]

            case insn.STORE | insn.STOREM:
                # Y: Store to the address field only at the destination.
                temp = self.memory[address] & ~insn.ADDRESS_MASK
                self.memory[address] = temp | (self.A & insn.ADDRESS_MASK)

            case insn.RETURN | insn.RETURNM:
                # T: Store the return address at the destination.
                temp = self.memory[address] & ~insn.ADDRESS_MASK
                temp2 = ((self.C + 1) & 4095) << insn.ADDRESS_SHIFT
                self.memory[address] = temp | temp2

            case insn.INPUT6:
                # I: Shift accumulator right 6 bits and input characters.
                # The manuals say the special shift is "I6200" but actual
                # paper tapes from the era use "I6300".  Accept both.
                if address >= 0xF80:
                    # Instruction is "I6200", which indicates a 6-bit
                    # shift without any input.
                    self.A = (self.A << 6) & 0xFFFFFFFE
                else:
                    self._input(track, 6)

            case insn.INPUT4:
                # I: Shift accumulator right 4 bits and input characters.
                if address >= 0xF80:
                    # Instruction is "-I6200", which indicates a 4-bit
                    # shift without any input.
                    self.A = (self.A << 4) & 0xFFFFFFFE
                else:
                    self._input(track, 4)

            case insn.DIV | insn.DIVM:
                # D: Divide the value in the accumulator by a value in memory.
                self.A, self.overflow = divide(self.A, self.memory[address])

            case insn.MUL_L | insn.MUL_LM:
                # N: Multiply memory with accumulator, return low word.
                self.A = multiply(self.A, self.memory[address], False)

            case insn.MUL_H | insn.MUL_HM:
                # M: Multiply memory with accumulator, return high word.
                self.A = multiply(self.A, self.memory[address], True)

            case insn.PRINT6:
                # P: Print the 6-bit character at the top of the accumulator.
                self._print(track, (self.A >> 26) & 0x3F)

            case insn.PRINT4:
                # P: Print the 4-bit character at the top of the accumulator
                # after converting it into a 6-bit character.
                self._print(track, ((self.A >> 26) & 0x3C) | 0x02)

            case insn.EXTRACT | insn.EXTRACTM:
                # E: Extract bits / bitwise AND.
                self.A = self.A & self.memory[address]

            case insn.UNCOND | insn.UNCONDM:
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

            case insn.HOLD | insn.HOLDM:
                # H: Hold / store the accumulator to memory.
                # Memory is 31-bit not 32-bit, so drop the LSB.
                self.memory[address] = self.A & 0xFFFFFFFE

            case insn.CLEAR | insn.CLEARM:
                # C: Store the accumulator to memory and then clear.
                self.memory[address] = self.A & 0xFFFFFFFE
                self.A = 0

            case insn.ADD | insn.ADDM:
                # A: Add the contents of memory to the accumulator.
                self.A, self.overflow = add(self.A, self.memory[address])

            case insn.SUB | insn.SUBM:
                # S: Subtract the contents of memory from the accumulator.
                self.A, self.overflow = sub(self.A, self.memory[address])

    '''
    Run the machine continuously until it halts.  Does nothing if the
    machine is already halted.
    '''
    def run(self):
        while not self.halted:
            self.step()

    '''
    Dump the contents of memory.
    '''
    def dump_memory(self):
        print("Addr      Word   Hex Word   Instruction Details")
        for address in range(0, len(self.memory)):
            word = self.memory[address]
            if word:
                inst = hexadecimal.to_hex(word, min_digits=1, order_codes=True)
                print("%02d%02d  %8s'  %s" % (address / 64, address % 64, inst, dis.disassemble(word)))

    '''
    Randomize the memory contents.
    '''
    def randomize_memory(self):
        random.seed()
        for address in range(0, len(self.memory)):
            self.memory[address] = random.randint(0, 0xFFFFFFFF)

    '''
    Print the word timings since startup.
    '''
    def print_time(self):
        rpm = 1125 # Speed of the disk motor in RPM.
        secs = self.word_times * (60.0 / rpm / 128.0)
        print("time: %d word times, %.2f seconds" % (self.word_times, secs));

    '''
    Internal handling for input instructions.
    '''
    def _input(self, device, bits):
        #Always shift (bits) zeros in first
        self.A = (self.A << bits) & 0xFFFFFFFF
        # Keep reading characters until we see a conditional stop.
        ch = self._input_char(device)
        while ch != 0x20:
            if ch != 0 and ch != 0x10: # Ignore Tape Feed and Carriage Return.
                if bits == 4:
                    ch >>= 2
                    self.A = (self.A << 4) | ch
                else:
                    self.A = (self.A << 6) | ch
            self.A = self.A & 0xFFFFFFFF
            ch = self._input_char(device)
        if self.verbose:
            # Print a newline in verbose mode after the word is input.
            print("")

    '''
    Input a single character.
    '''
    def _input_char(self, device):
        if device == 0:
            # Read from the tape reader.
            if self.tape_posn < len(self.tape):
                ch = self.tape[self.tape_posn]
                self.tape_posn += 1
                return ch
            else:
                # Tape is exhausted, end with a conditional stop.
                return 0x20
        elif device == 2:
            # Read from the typewriter.
            if len(self.pre_typed_input) > 0:
                # Read from the tape image that was loaded at startup.
                ch = self.pre_typed_input[0]
                self.pre_typed_input = self.pre_typed_input[1:]
                return ch

            if self.input_buffer != -1:
                # Buffered character from last time.
                ch = self.input_buffer
                self.input_buffer = -1
                return ch

            if sys.stdin.isatty():
                data = readchar.readchar()
            else:
                data = sys.stdin.read(1)

            if data == readchar.key.CTRL_C:
                raise KeyboardInterrupt
            elif data == readchar.key.ESC:
                # ESC dumps the contents of memory.
                self.dump_memory()
            elif data:
                if data != '\'': #Dont echo cond stop
                    print(data, end='\n' if data == '\r' else '', flush=True) # Echo the typewriter input.
                codes = charset.io_ascii_to_6bit(data, upper=self.input_upper, as_list=True)
                if len(codes) > 1 and codes[0] == 0x04:
                    # Shift to lower case.
                    self.input_upper = False
                    self.input_buffer = codes[1]
                    return codes[0]
                elif len(codes) > 1 and codes[0] == 0x08:
                    # Shift to upper case.
                    self.input_upper = True
                    self.input_buffer = codes[1]
                    return codes[0]
                elif len(codes) > 0:
                    return codes[0]
            return 0 # Return "Tape Feed" if the character cannot be mapped.
        else:
            # Unknown device: return a conditional stop.
            return 0x20

    '''
    Internal routine to print a single charater to a device.
    '''
    def _print(self, device, ch):
        if device == 2:
            if self.print_color:
                print("\033[31m", end='', flush=True)
            # Print to the typewriter.
            if ch == 0x04:
                # Shift to lower case.
                self.print_upper = False
            elif ch == 0x08:
                # Shift to upper case.
                self.print_upper = True
            elif ch == 0x10:
                # Carriage return.
                print("", flush=True)
            elif ch == 0x12 and self.print_upper:
                # Delta character.
                print('\u0394', end='')
            elif ch == 0x1E and self.print_upper:
                # Pi character.
                print('\u03C0', end='')
            elif ch == 0x22 and self.print_upper:
                # Sigma character.
                print('\u03A3', end='')
            elif ch == 0x0C:
                # Color Shift
                self.print_color = not self.print_color
            elif ch == 0x3f:
                # Don't print delete
                pass
            else:
                # Some other character.
                print(charset.io_6bit_to_ascii(ch, upper=self.print_upper), end='', flush=True)
            print("\033[0m", end='', flush=True)
        elif device == 6:
            # Print to the tape punch.
            # TODO
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass  # readchar manages terminal state internally; nothing to restore.
