
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

import sys
import lgp21.hexadecimal as hexadecimal
import lgp21.insn as insn

'''
Converts the decimal form of an address to the hexadecimal form.
Returns None if the decimal form cannot be converted.
'''
def dec_to_hex_address(value):
    if value < 0 or value > 6363:
        return None
    track = int(value / 100)
    sector = int(value % 100)
    if track > 63 or sector > 63:
        return None
    return track * 64 + sector

'''
Determine if an instruction can be emitted into the final image.
'''
def can_emit(insn):
    return insn != None and insn.emit

'''
Details about an instruction for the code generator, which may be
partially instantiated if labels have not yet been resolved.
'''
class Instruction:
    '''
    Constructs a new instruction at a specific location in the source file.
    '''
    def __init__(self, location):
        self.word = 0
        self.relocatable = False
        self.literal = False
        self.expr = None
        self.location = location
        self.emit = True

    '''
    Sets the order code for this instruction and clear the other fields.
    '''
    def set_order(self, order):
        self.word = order
        self.relocatable = False
        self.literal = False
        self.expr = None
        self.offset = 0

    '''
    Sets the address field for this instruction to an expression.
    '''
    def set_address(self, expr):
        self.relocatable = False
        self.literal = False
        self.expr = expr

    '''
    Sets this instruction to a literal word value.
    '''
    def set_literal(self, word):
        self.word = word
        self.relocatable = False
        self.literal = True
        self.expr = None

    '''
    Resolves label references in this instruction.  Returns False if any
    of the labels are undefined.
    '''
    def resolve(self, code):
        if self.expr != None:
            etype, address = self.expr.eval(code)
            match etype:
                case 'undef':
                    code.error(self.location, "undefined label `%s'" % address)
                    return False

                case 'address':
                    if address < 0 or address > 4095:
                        code.error(self.location, 'address is out of range')
                        return False
                    self.word = (self.word & ~insn.ADDRESS_MASK) | (address << insn.ADDRESS_SHIFT)
                    self.relocatable = self.expr.has_labels()

                case _:
                    code.error(self.location, 'address operand required')
                    return False
        return True

    '''
    Formats this instruction for the final tape image.
    '''
    def format(self, raw=False):
        if self.literal:
            return hexadecimal.to_hex(self.word) + "'"
        elif raw:
            return hexadecimal.to_hex(self.word, min_digits=1) + "'"
        if (self.word & 0x80000000) != 0:
            if self.relocatable:
                prefix = '800'
            else:
                prefix = '80x'
        elif self.relocatable:
            prefix = ''
        else:
            prefix = 'x'
        order = (self.word & 0x000F0000) >> insn.ORDER_SHIFT
        track = (self.word & insn.TRACK_MASK) >> insn.TRACK_SHIFT
        sector = (self.word & insn.SECTOR_MASK) >> insn.SECTOR_SHIFT
        return prefix + hexadecimal.order_chars[order] + ('%02d%02d' % (track, sector)) + "'"

'''
Support class for generating LGP-21 code from assemblers and compilers.
'''
class CodeGenerator:
    '''
    Initialises the code generator.
    '''
    def __init__(self):
        self.memory = [None] * 4096
        self.PC = 0
        self.labels = {}
        self.entry_point = None
        self.relocatable = False
        self.errors = False
        self.emit = True
        self.lines = []

    '''
    Adds an instruction at the current PC and advances the PC.
    '''
    def add_instruction(self, insn):
        insn.emit = self.emit
        if self.memory[self.PC] != None:
            self.error(insn.location, 'code overwritten at %02d%02d' % (self.PC / 64, self.PC % 64))
        self.memory[self.PC] = insn
        if len(self.lines) > 0:
            self.lines[len(self.lines) - 1]['addresses'].append(self.PC)
        self.PC = (self.PC + 1) & 4095

    '''
    Gets a label definition for the current location in the program.
    Returns None if the label was already defined.
    '''
    def label_for_PC(self, name, location):
        if name in self.labels:
            # We may have seen this label before in a forward reference.
            label = self.labels[name]
            if 'address' in label or 'value' in label:
                # Label is already defined.
                return None
            label['address'] = self.PC
            label['location'] = location
        else:
            label = {'name': name, 'address': self.PC, 'location': location}
            self.labels[name] = label
        return label

    '''
    Sets a label to an explicit value.  Used for equate symbols.
    Returns None if the label was already defined
    '''
    def set_label(self, name, value, location):
        if name in self.labels:
            # We have seen this label before.  Already defined or forward ref?
            label = self.labels[name]
            if 'value' in label or 'address' in label:
                # Label is already defined.
                return None
            label['value'] = value
            label['location'] = location
        else:
            label = {'name': name, 'value': value, 'location': location}
            self.labels[name] = label
        return label

    '''
    Sets a label to an explicit address value.  Used for equate symbols.
    Returns None if the label was already defined
    '''
    def set_label_address(self, name, value, location):
        if name in self.labels:
            # We have seen this label before.  Already defined or forward ref?
            label = self.labels[name]
            if 'value' in label or 'address' in label:
                # Label is already defined.
                return None
            label['address'] = value
            label['location'] = location
        else:
            label = {'name': name, 'address': value, 'location': location}
            self.labels[name] = label
        return label

    '''
    Gets a previously defined label or a forward reference to a future label.
    '''
    def get_label(self, name, location):
        if name in self.labels:
            label = self.labels[name]
        else:
            label = {'name': name, 'location': location}
            self.labels[name] = label
        return label

    '''
    Set the entry point label for the program.
    '''
    def set_entry_point(self, label):
        self.entry_point = label

    '''
    Resolve all labels in all instructions and create the final words
    to be written to the output tape.  Returns False if there was an error.
    '''
    def resolve(self):
        ok = True
        for insn in self.memory:
            if insn != None:
                if insn.resolve(self):
                    # If the word has the LSB set, then it cannot be
                    # stored in memory successfully.  Warn about this.
                    if (insn.word & 1) != 0:
                        self.warning(insn.location, 'word with LSB set')
                else:
                    ok = False
        if self.entry_point != None:
            # Check that the entry point label has been resolved.
            label = self.entry_point
            if not ('address' in label) and not ('value' in label):
                self.error(label['location'], "undefined label `%s'" % label['name'])
                ok = False
        return ok

    '''
    Converts the final program into a tape image in ASCII.
    It is assumed that resolve() has already been run successfully.
    '''
    def to_tape(self, max_words_per_line=8):
        # Start with an empty tape.
        tape = ''

        # Output each run of contiguous words.
        address = 0
        while address < len(self.memory):
            # Skip unusued instructions to find the next run.
            while address < len(self.memory) and not can_emit(self.memory[address]):
                address += 1
            if address >= len(self.memory):
                # No more runs in the program.
                break

            # Write the origin definition for this run.
            if not self.relocatable:
                tape += ";000%02d%02d'" % (address / 64, address % 64)
                if max_words_per_line <= 1:
                    tape += '\n'
                tape += "/0000000'"
                word_count = 2
            else:
                word_count = 0

            # Output the words in the run.
            while address < len(self.memory) and can_emit(self.memory[address]):
                insn = self.memory[address]
                if insn.literal:
                    # Output a run of literal words, maximum of 63 words.
                    count = 1
                    while count < 63 and (address + count) < len(self.memory) and can_emit(self.memory[address + count]) and self.memory[address + count].literal:
                        count += 1
                    if word_count >= max_words_per_line:
                        tape += '\n'
                        word_count = 0
                    tape += ",00000%02d'" % count
                    word_count += 1
                    while count > 0:
                        if word_count >= max_words_per_line:
                            tape += '\n'
                            word_count = 0
                        tape += self.memory[address].format()
                        word_count += 1
                        address += 1
                        count -= 1
                else:
                    # Output a standard instruction.
                    if word_count >= max_words_per_line:
                        tape += '\n'
                        word_count = 0
                    tape += insn.format()
                    word_count += 1
                    address += 1
            if word_count != 0:
                tape += '\n'

        # Jump to the entry point if we have one.
        if self.entry_point != None and not self.relocatable:
            if 'address' in self.entry_point:
                address = self.entry_point['address']
            elif 'value' in self.entry_point:
                address = self.entry_point['value']
            address = address & 4095
            tape += ".000%02d%02d'\n" % (address / 64, address % 64)
            pass

        # Tape is ready to go.
        return tape

    '''
    Converts the final program into a self-bootstraping tape image in ASCII.
    It is assumed that resolve() has already been run successfully.

    "bootstrap_addr" is the address to write the bootstrap to, usually track 63.
    "device" should be 0 for the tape reader or 2 for the typewriter.
    '''
    def to_bootstrap_tape(self, bootstrap_addr=63*64, device=2, max_words_per_line=8, compact=False):
        # Find the min and max addresses that are occupied by the program.
        min_addr = 0
        max_addr = 4095
        while min_addr < 4096 and not can_emit(self.memory[min_addr]):
            min_addr += 1
        while max_addr >= 0 and not can_emit(self.memory[max_addr]):
            max_addr -= 1
        if min_addr > max_addr:
            # Program is empty.
            return ''

        #
        # Build the part of the bootstrap that is manually entered
        # at the nominal location of track 63, sector 0:
        #
        #   000c6300'800i0200'
        #   000c6301'000c6303'
        #   000c6302'800i0200'
        #   000u6300'normal        '
        #
        words = [
            0x000D0000 + (bootstrap_addr << insn.ADDRESS_SHIFT),
            0x80040000 + (device << 8),
            0x000D0000 + ((bootstrap_addr + 1) << insn.ADDRESS_SHIFT),
            0x000D0000 + ((bootstrap_addr + 3) << insn.ADDRESS_SHIFT),
            0x000D0000 + ((bootstrap_addr + 2) << insn.ADDRESS_SHIFT),
            0x80040000 + (device << 8),
            0x000A0000 + (bootstrap_addr << insn.ADDRESS_SHIFT)
        ]
        word_count = 0
        tape = ''
        for word in words:
            tape += hexadecimal.to_hex(word, order_codes=True) + "'"
            word_count += 1
            if word_count >= 2 or word_count >= max_words_per_line:
                tape += '\n'
                word_count = 0
        tape += "normal        '\n\n"

        #
        # Continue building the bootstrap code:
        #
        #   000c6304'u6300'
        #   000c6305'800i0200'
        #   000c6306'gwc0000'   ; Replaced with starting address and count.
        #   000c6307'b6306'
        #   000c6308's6313'
        #   000c6309't6312'
        #   000c6310'c6306'
        #   000c6311'u6305'
        #   000c6312'uxxxx'     ; Jump to program entry point (or halt if none).
        #   000c6313'wwwwj'
        #   000u6305''
        #
        count = max_addr - min_addr
        if self.entry_point != None:
            if 'address' in self.entry_point:
                address = self.entry_point['address']
            elif 'value' in self.entry_point:
                address = self.entry_point['value']
            address = address & 4095
            entry_point_word = 0x000A0000 + (address << insn.ADDRESS_SHIFT)
        else:
            entry_point_word = 0
        if compact:
            # Use the compact form of the bootstrap where the main code
            # is explicitly written using word pairs.
            words = [
                0x000D0000 + ((bootstrap_addr + 4) << insn.ADDRESS_SHIFT),
                0x000A0000 + (bootstrap_addr << insn.ADDRESS_SHIFT),
            ]
        else:
            words = [
                0x000D0000 + ((bootstrap_addr + 4) << insn.ADDRESS_SHIFT),
                0x000A0000 + (bootstrap_addr << insn.ADDRESS_SHIFT),
                0x000D0000 + ((bootstrap_addr + 5) << insn.ADDRESS_SHIFT),
                0x80040000 + (device << 8),
                0x000D0000 + ((bootstrap_addr + 6) << insn.ADDRESS_SHIFT),
                0x000D0000 + (min_addr << insn.ADDRESS_SHIFT) + (count << 20),
                0x000D0000 + ((bootstrap_addr + 7) << insn.ADDRESS_SHIFT),
                0x00010000 + ((bootstrap_addr + 6) << insn.ADDRESS_SHIFT),
                0x000D0000 + ((bootstrap_addr + 8) << insn.ADDRESS_SHIFT),
                0x000F0000 + ((bootstrap_addr + 13) << insn.ADDRESS_SHIFT),
                0x000D0000 + ((bootstrap_addr + 9) << insn.ADDRESS_SHIFT),
                0x000B0000 + ((bootstrap_addr + 12) << insn.ADDRESS_SHIFT),
                0x000D0000 + ((bootstrap_addr + 10) << insn.ADDRESS_SHIFT),
                0x000D0000 + ((bootstrap_addr + 6) << insn.ADDRESS_SHIFT),
                0x000D0000 + ((bootstrap_addr + 11) << insn.ADDRESS_SHIFT),
                0x000A0000 + ((bootstrap_addr + 5) << insn.ADDRESS_SHIFT),
                0x000D0000 + ((bootstrap_addr + 12) << insn.ADDRESS_SHIFT),
                entry_point_word,
                0x000D0000 + ((bootstrap_addr + 13) << insn.ADDRESS_SHIFT),
                0x000FFFFC,
                0x000A0000 + ((bootstrap_addr + 5) << insn.ADDRESS_SHIFT),
                0x00000000
            ]
        word_count = 0
        first = True
        for word in words:
            if first:
                tape += hexadecimal.to_hex(word, order_codes=True) + "'"
                first = False
            elif word == 0x000FFFFC:
                tape += hexadecimal.to_hex(word, min_digits=0, order_codes=False) + "'"
            else:
                tape += hexadecimal.to_hex(word, min_digits=0, order_codes=True) + "'"
            word_count += 1
            if word_count >= max_words_per_line:
                tape += '\n'
                word_count = 0
        if word_count > 0:
            tape += '\n'
            word_count = 0

        # Append the actual words of the program to the tape.
        for address in range(min_addr, max_addr+1):
            inst = self.memory[address]
            if compact:
                # Compact form needs a "Cxxxx" instruction to deposit
                # each word of the program into memory.
                deposit = 0x000D0000 + (address << insn.ADDRESS_SHIFT)
                tape += hexadecimal.to_hex(deposit, min_digits=0, order_codes=True) + "'"
                word_count += 1
                if word_count >= max_words_per_line:
                    tape += '\n'
                    word_count = 0
            if can_emit(inst):
                word = inst.word
                if inst.literal:
                    tape += hexadecimal.to_hex(word, min_digits=0, order_codes=False) + "'"
                else:
                    tape += hexadecimal.to_hex(word, min_digits=0, order_codes=True) + "'"
            else:
                # Cannot emit this word, but we need something, so write zero.
                tape += "'"
            word_count += 1
            if word_count >= max_words_per_line:
                tape += '\n'
                word_count = 0
        if compact:
            # Jump to the program entry point in compact mode.
            tape += hexadecimal.to_hex(entry_point_word, min_digits=0, order_codes=True) + "''"
        if word_count > 0:
            tape += '\n'
        return tape

    '''
    Report an error.
    '''
    def error(self, location, message):
        sys.stderr.write('%s: %s\n' % (location, message))
        self.errors = True

    '''
    Report a warning.
    '''
    def warning(self, location, message):
        sys.stderr.write('%s: warning: %s\n' % (location, message))

    '''
    Add a source line for the listing.
    '''
    def add_line(self, line, number):
        self.lines.append({'text': line, 'linenum': number, 'addresses': []})
