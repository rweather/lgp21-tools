
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

import os
import re
import sys
import lgp21.charset as charset
import lgp21.codegen as codegen
import lgp21.expr as expr
import lgp21.hexadecimal as hexadecimal
import lgp21.insn as insn

alpha_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
alphanum_chars = alpha_chars + '0123456789'

'''
Determine if a label name is valid.
'''
def is_valid_label(name):
    global alpha_chars
    global alphanum_chars
    if len(name) == 0:
        return False
    first = True
    for ch in name:
        if first:
            if not ch in alpha_chars:
                return False
            first = False
        elif not ch in alphanum_chars:
            return False
    return True

'''
Determine if the start of a line looks like an address label.
Returns None if not an address label, or the address.
The first character of "line" is assumed to be ".".
'''
def to_address_label(line):
    if len(line) <= 1:
        return None
    posn = 1
    address = 0
    while posn < len(line) and line[posn] >= '0' and line[posn] <= '9':
        address = int(address * 10 + int(line[posn]))
        posn += 1
    if posn > 1 and address <= 6363:
        track = int(address / 100)
        sector = int(address % 100)
        if track < 64 and sector < 64:
            if posn < len(line) and line[posn] == ':':
                return (address, line[posn+1:])
    return None

'''
Split a line the next whitespace character.
'''
def split_line(line):
    posn = line.find(' ')
    if posn < 0:
        posn = line.find('\t')
        if posn < 0:
            return line, ''
    return line[:posn], line[posn+1:].strip()

'''
Assemble literal words into the program.
'''
def assemble_words(code, location, line):
    # Parse the comma-separated words on the line as a list.
    words = expr.parse_expression(code, location, line, as_list=True)
    if words == None:
        # Error parsing the expression list.
        return

    # Generate the words into the program.
    for expression in words:
        kind, value = expression.eval(code)
        insn = codegen.Instruction(location)
        if expression.has_labels():
            # If the expression looks like a label address, convert it
            # into a "0" order with the address in the right place.
            insn.set_order(0)
            insn.set_address(expression)
        else:
            match kind:
                case 'address':
                    insn.set_literal(value << 2)

                case 'int':
                    if value < -0x8000000 or value > 0xFFFFFFFF:
                        code.error(location, 'integer value is out of range')
                    else:
                        insn.set_literal(value & 0xFFFFFFFF)

                case 'float':
                    if value < -1.0 or value >= 1.0:
                        code.error(location, 'floating-point value is out of range')
                    else:
                        # Scale the floating-point value and set the LSB to 0.
                        insn.set_literal((int(value * 2147483648)) & 0xFFFFFFFE)

                case 'string':
                    # Convert the string into 6-bit characters, 5 at a time.
                    chars = charset.io_ascii_to_6bit(value, as_list=True, end_in_lower=True)
                    while (len(chars) % 5) != 0:
                        chars.append(0)
                    for index in range(0, len(chars), 5):
                        word  = int(chars[index]) << 26
                        word |= int(chars[index + 1]) << 20
                        word |= int(chars[index + 2]) << 14
                        word |= int(chars[index + 3]) << 8
                        word |= int(chars[index + 4]) << 2
                        insn = codegen.Instruction(location)
                        insn.set_literal(word)
                        code.add_instruction(insn)
                    continue

                case _:
                    code.error(location, 'cannot evaluate expression')
                    return
        code.add_instruction(insn)

'''
Assemble a directive.
'''
def assemble_directive(code, location, line):
    # Do we have a ".NNNN:" address label on the start of the line?
    # If so, adjust the origin and process the rest of the line.
    # This is for direct placement of instructions and data in memory.
    address = to_address_label(line)
    if address != None:
        line = address[1].strip()
        code.PC = codegen.dec_to_hex_address(address[0])
        if len(line) == 0:
            return
        if line.startswith('.'):
            assemble_directive(code, location, line)
        elif line.find(':') >= 0:
            assemble_label(code, location, line)
        else:
            assemble_instruction(code, location, line)
        return

    # Determine what kind of directive we have.
    name, args = split_line(line)
    match name:
        case '.org':
            # Set a new origin.
            orgexpr = expr.parse_expression(code, location, args)
            if orgexpr != None:
                kind, value = orgexpr.eval(code)
                if kind != 'address':
                    code.error(location, 'origin must be a address')
                else:
                    code.PC = value

        case '.entry':
            # Set the entry point for the program.  Must be a label.
            entexpr = expr.parse_expression(code, location, args)
            if entexpr != None:
                if type(entexpr) is expr.LabelExpression:
                    code.set_entry_point(entexpr.label)
                else:
                    code.error(location, 'entry point must be a label')

        case '.dw':
            # Emit literal words into the program.
            assemble_words(code, location, args)

        case '.noemit':
            # Stop emitting code.
            code.emit = False

        case '.emit':
            # Start emitting code.
            code.emit = True

        case '.include':
            # Include another file at this location.
            current_filename = code.filename
            assemble_input(code, os.path.join(os.path.dirname(current_filename), args))
            code.filename = current_filename

        case _:
            code.error(location, "unknown directive `%s'" % name)

# Properties of all opcodes and aliases.
opcodes = {
    'a':    { 'order': insn.ADD },
    'add':  { 'order': insn.ADD },
    'b':    { 'order': insn.BRING },
    'ld':   { 'order': insn.BRING },
    'c':    { 'order': insn.CLEAR },
    'clr':  { 'order': insn.CLEAR },
    'stc':  { 'order': insn.CLEAR },
    'd':    { 'order': insn.DIV },
    'div':  { 'order': insn.DIV },
    'e':    { 'order': insn.EXTRACT },
    'and':  { 'order': insn.EXTRACT },
    'h':    { 'order': insn.HOLD },
    'st':   { 'order': insn.HOLD },
    'i':    { 'order': insn.INPUT6 },
    'in6':  { 'order': insn.INPUT6, 'defarg': '0200' },
    'shl6': { 'order': insn.INPUT6, 'arg': '6200' },
    '-i':   { 'order': insn.INPUT4 },
    '-in4': { 'order': insn.INPUT4, 'defarg': '0200' },
    'shl4': { 'order': insn.INPUT4, 'arg': '6200' },
    'm':    { 'order': insn.MUL_H },
    'mulh': { 'order': insn.MUL_H },
    'n':    { 'order': insn.MUL_L },
    'mull': { 'order': insn.MUL_L },
    'p':    { 'order': insn.PRINT6 },
    'pr6':  { 'order': insn.PRINT6, 'defarg': '0200' },
    '-p':   { 'order': insn.PRINT4 },
    'pr4':  { 'order': insn.PRINT4, 'defarg': '0200' },
    'r':    { 'order': insn.RETURN },
    'sret': { 'order': insn.RETURN },
    's':    { 'order': insn.SUB },
    'sub':  { 'order': insn.SUB },
    't':    { 'order': insn.COND },
    'jn':   { 'order': insn.COND },
    '-t':   { 'order': insn.CTRL },
    'jnt':  { 'order': insn.CTRL },
    'u':    { 'order': insn.UNCOND },
    'jmp':  { 'order': insn.UNCOND },
    'y':    { 'order': insn.STORE },
    'sta':  { 'order': insn.STORE },
    'z':    { 'order': insn.STOP },
    'hlt':  { 'order': insn.STOP, 'arg': '0000' },
    'nop':  { 'order': insn.STOP, 'arg': '0200' },
    '-z':   { 'order': insn.OVERFLOW },
    'ovr':  { 'order': insn.OVERFLOW },
}

'''
Assemble an instruction.
'''
def assemble_instruction(code, location, line):
    global opcodes

    # Break the line up into name and arguments.
    name, operand = split_line(line)
    name = name.lower()
    if not name in opcodes:
        code.error(location, "unknown opcode `%s'" % name)
        return
    info = opcodes[name]
    if 'arg' in info:
        # Operand is implicit, so insn must not have a user-specifed operand.
        if len(operand) > 0:
            code.error(location, "opcode `%s' does not take operands" % name)
            return
        operand = info['arg']
    elif 'defarg' in info and len(operand) == 0:
        # Set the default operand.
        operand = info['defarg']

    # Parse the operand expression.
    operand_expr = expr.parse_expression(code, location, operand)
    if operand_expr == None:
        # An error was reported while parsing the operand.
        # Set the address field to zero and continue.
        operand_expr = expr.AddressExpression(0)

    # Construct the instruction and add it to the code.
    insn = codegen.Instruction(location)
    insn.set_order(info['order'])
    insn.set_address(operand_expr)
    code.add_instruction(insn)

'''
Assemble a "label = value" equate.
'''
def assemble_equate(code, location, name, text):
    eqexpr = expr.parse_expression(code, location, text)
    if eqexpr != None:
        kind, value = eqexpr.eval(code)
        match kind:
            case 'address':
                label = code.set_label_address(name, value, location)
                if label == None:
                    code.error(location, "label `%s' is already defined" % name)

            case 'int':
                label = code.set_label(name, value, location)
                if label == None:
                    code.error(location, "label `%s' is already defined" % name)

            case 'float' | 'string':
                code.error(location, 'cannot set labels to this type of value')

            case _:
                code.error(location, 'cannot evaluate the value at this point')

'''
Assemble a label, optionally followed by an instruction or equate value.
'''
def assemble_label(code, location, line):
    posn = line.find(':')
    if posn < 0:
        posn = line.find('=')
        if posn < 0:
            code.error(location, 'label name must be followed by a colon')
            return
        else:
            name = line[:posn].strip()
            if not is_valid_label(name):
                code.error(location, "`%s' is not a valid label name" % name)
                return
            assemble_equate(code, location, name, line[posn+1:].strip())
            return
    name = line[:posn].strip()
    if not is_valid_label(name):
        code.error(location, "`%s' is not a valid label name" % name)
        return
    if not code.label_for_PC(name, location):
        code.error(location, "`%s' is already defined" % name)
        return
    rest = line[posn+1:].strip()
    if rest.startswith("."):
        assemble_directive(code, location, rest)
    elif len(rest) > 0:
        assemble_instruction(code, location, rest)

'''
Process a single line of assembly source.
'''
def assemble_line(code, location, line):
    # Strip comments and whitespace from the line.
    posn = line.find(';')
    if posn >= 0:
        line = line[:posn]
    line = line.rstrip()
    if len(line) == 0:
        # Ignore empty lines.
        return

    # Assemble the line based on its type.
    line2 = line.lstrip()
    if line2.startswith('.'):
        assemble_directive(code, location, line2)
    elif line != line2:
        assemble_instruction(code, location, line2)
    else:
        assemble_label(code, location, line)

'''
Process an input assembly source code file.
'''
def assemble_input(code, filename):
    try:
        code.filename = filename
        with open(filename, 'r') as file:
            line_number = 0
            for line in file:
                line_number += 1
                location = filename + ':' + str(line_number)
                assemble_line(code, location, line)
    except OSError:
        code.error(filename, 'could not read source file')
