
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

import re
import sys
import lgp21.hexadecimal as hexadecimal
import lgp21.codegen as codegen

'''
Base class for expressions.
'''
class Expression:
    def __init__(self, kind):
        self.kind = kind

    def eval(self, context):
        return 'error', None

    def has_labels(self):
        return False

'''
Integer expressions.
'''
class IntegerExpression(Expression):
    def __init__(self, value):
        super().__init__('int')
        self.value = value

    def eval(self, context):
        return 'int', self.value

'''
Address expressions.
'''
class AddressExpression(Expression):
    def __init__(self, value):
        super().__init__('address')
        self.value = value

    def eval(self, context):
        # Shift the track/sector address into position.
        return 'address', self.value

'''
String expressions.
'''
class StringExpression(Expression):
    def __init__(self, value):
        super().__init__('string')
        self.value = value

    def eval(self, context):
        return 'string', self.value

'''
Floatint-point constant expressions.
'''
class FloatExpression(Expression):
    def __init__(self, value):
        super().__init__('float')
        self.value = value

    def eval(self, context):
        return 'float', self.value

'''
Unary expresions.
'''
class UnaryExpression(Expression):
    def __init__(self, kind, subexpr):
        super().__init__(kind)
        self.subexpr = subexpr

    def has_labels(self):
        return self.subexpr.has_labels()

'''
Binary expresions.
'''
class BinaryExpression(Expression):
    def __init__(self, kind, left, right):
        super().__init__(kind)
        self.left = left
        self.right = right

    def has_labels(self):
        return self.left.has_labels() or self.right.has_labels()

'''
Add expressions.
'''
class AddExpression(BinaryExpression):
    def __init__(self, left, right):
        super().__init__('add', left, right)

    def eval(self, context):
        left = self.left.eval(context)
        right = self.right.eval(context)
        if left[0] == 'address' and right[0] == 'address':
            return 'address', left[1] + right[1]
        elif left[0] == 'int' and right[0] == 'int':
            return 'int', left[1] + right[1]
        elif left[0] == 'float' and (right[0] == 'int' or right[0] == 'float'):
            return 'float', left[1] + right[1]
        elif left[0] == 'int' and right[0] == 'float':
            return 'float', left[1] + right[1]
        elif left[0] == 'string' and right[0] == 'string':
            return 'string', left[1] + right[1]
        elif left[0] == 'undef':
            return left
        elif right[0] == 'undef':
            return right
        else:
            return 'error', None

'''
Subtract expressions.
'''
class SubExpression(BinaryExpression):
    def __init__(self, left, right):
        super().__init__('sub', left, right)

    def eval(self, context):
        left = self.left.eval(context)
        right = self.right.eval(context)
        if left[0] == 'address' and right[0] == 'address':
            return 'address', left[1] - right[1]
        elif left[0] == 'int' and right[0] == 'int':
            return 'int', left[1] - right[1]
        elif left[0] == 'float' and (right[0] == 'int' or right[0] == 'float'):
            return 'float', left[1] - right[1]
        elif left[0] == 'int' and right[0] == 'float':
            return 'float', left[1] - right[1]
        elif left[0] == 'undef':
            return left
        elif right[0] == 'undef':
            return right
        else:
            return 'error', None

'''
Negate expressions.
'''
class NegExpression(UnaryExpression):
    def __init__(self, subexpr):
        super().__init__('neg', subexpr)

    def eval(self, context):
        subexpr = self.subexpr.eval(context)
        if subexpr[0] == 'int':
            return 'int', -subexpr[1]
        elif subexpr[0] == 'float':
            return 'float', -subexpr[1]
        elif subexpr[0] == 'undef':
            return subexpr
        else:
            return 'error', None

'''
Label reference.
'''
class LabelExpression(Expression):
    def __init__(self, label):
        super().__init__('label')
        self.label = label

    def eval(self, context):
        if 'value' in self.label:
            return 'int', self.label['value']
        elif 'address' in self.label:
            return 'address', self.label['address']
        else:
            return 'undef', self.label['name']

    def has_labels(self):
        return True

'''
Remove escape sequences from a string token.
'''
def unescape_string(value):
    result = ''
    escape = False
    for ch in value:
        if escape:
            match ch:
                case 'b':
                    result += '\b'
                case 'n':
                    result += '\n'
                case 't':
                    result += '\t'
                case _:
                    result += ch
            escape = False
        elif ch == '\\':
            escape = True
        else:
            result += ch
    return result

'''
Parse a basic unary expression.
'''
def parse_basic_expression(code, location, tokens):
    if len(tokens) == 0:
        code.error(location, 'expression expected')
        return None, tokens
    token = tokens[0]
    tokens = tokens[1:]
    match token[0]:
        case 'ID':
            # Reference to a named label.
            return LabelExpression(code.get_label(token[1], location)), tokens
        case 'FLOAT':
            # Floating-point constant.
            return FloatExpression(float(token[1])), tokens
        case 'ADDRESS':
            # LGP-21 track/sector address constant like 0300, 6317, etc.
            dec = codegen.dec_to_hex_address(int(token[1], 10))
            if dec == None:
                code.error(location, "address `%s' is out of range" % token)
                return None, tokens
            return AddressExpression(dec), tokens
        case 'DECIMAL':
            # Regular decimal.
            return IntegerExpression(int(token[1][1:], 10)), tokens
        case 'HEX1':
            # Regular hexadecimal.
            return IntegerExpression(int(token[1][1:], 16)), tokens
        case 'HEX2':
            # LGP-21 hexadecimal.
            return IntegerExpression(hexadecimal.from_hex(token[1][1:])), tokens
        case 'STR1' | 'STR2':
            # Quoted string.
            return StringExpression(unescape_string(token[1][1:-1])), tokens
        case 'SUB':
            # Negate the expression that follows.
            expr = parse_basic_expression(code, location, tokens)
            if expr[0] == None:
                return expr
            return NegExpression(expr[0]), expr[1]
        case 'PC':
            # "*" is a reference to the current program counter.
            return AddressExpression(code.PC), tokens
        case 'COMMA' | 'ADD':
            # This token is not allowed to start a basic expression.
            code.error(location, "unexpected token `%s'" % token[1])
            return None, tokens

'''
Parse an additive expression.  Note: The result is right-associative.
'''
def parse_additive_expression(code, location, tokens):
    left, tokens = parse_basic_expression(code, location, tokens)
    if left == None or len(tokens) == 0:
        return left, tokens
    if tokens[0][0] != 'ADD' and tokens[0][0] != 'SUB':
        return left, tokens
    if tokens[0][0] == 'ADD':
        right, tokens = parse_additive_expression(code, location, tokens[1:])
        if right == None:
            return right, tokens
        return AddExpression(left, right), tokens
    else:
        right, tokens = parse_additive_expression(code, location, tokens[1:])
        if right == None:
            return right, tokens
        return SubExpression(left, right), tokens

'''
Parse a whole expression with no tokens left over.
'''
def parse_whole_expression(code, location, tokens):
    expr, tokens = parse_additive_expression(code, location, tokens)
    if len(tokens) != 0 and expr != None:
        code.error(location, "extra tokens on line")
    return expr

'''
Parse a comma-separated list of expressions.
'''
def parse_list_expression(code, location, tokens):
    expr, tokens = parse_additive_expression(code, location, tokens)
    if expr == None:
        return None
    expr_list = [expr]
    while len(tokens) != 0 and tokens[0][0] == 'COMMA':
        tokens = tokens[1:]
        expr, tokens = parse_additive_expression(code, location, tokens)
        if expr == None:
            return None
        expr_list.append(expr)
    if len(tokens) != 0:
        code.error(location, "missing comma between expressions")
        return None
    return expr_list

# Token details for expressions.  Based on:
# https://docs.python.org/3/library/re.html#writing-a-tokenizer
tokens = [
    ('ID',      r'[a-zA-Z_][0-9a-zA-Z_]*'),
    ('FLOAT',   r'[0-9]+\.[0-9]*'),
    ('ADDRESS', r'[0-9]+'),
    ('DECIMAL', r'#-?[0-9]+'),
    ('HEX1',    r'\$[0-9A-Fa-f]+'),
    ('HEX2',    r'&[0-9fgjkqwFGJKQW]+'),
    ('STR1',    r'"([^\\"]|\\[bnt"' + r"'" + r'])*"'),
    ('STR2',    r"'([^\\']|\\[bnt'" + r'"' + r"])*'"),
    ('ADD',     r'\+'),
    ('SUB',     r'-'),
    ('PC',      r'\*'),
    ('WS',      r'\s'),
    ('COMMA',   r','),
    ('ERROR',   r'.')
]
token_regex = re.compile('|'.join('(?P<%s>%s)' % pair for pair in tokens))

'''
Parse an expression.
'''
def parse_expression(code, location, line, as_list=False):
    global token_regex

    # Break the line up into tokens.
    tokens = []
    for x in token_regex.finditer(line):
        kind = x.lastgroup
        value = x.group()
        if kind == 'WS':
            continue
        elif kind == 'ERROR':
            code.error(location, "unknown token `%s' in expression" % value)
            return None
        tokens.append((kind, value))

    # Perform syntactic analysis to determine what the expression is.
    if as_list:
        return parse_list_expression(code, location, tokens)
    else:
        return parse_whole_expression(code, location, tokens)
