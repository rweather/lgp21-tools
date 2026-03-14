
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

# Characters that represent hexadecimal digits.  Lower case is preferred.
hex_chars = '0123456789fgjkqw'
hex_chars_upper = '0123456789FGJKQW'

# Characters that represent instruction orders.
order_chars = 'zbyridnmpeuthcas'
order_chars_upper = 'ZBYRIDNMPEUTHCAS'

'''
Convert an integer value into a hexadecimal string.
'''
def to_hex(v, min_digits=8, order_codes=False):
    global hex_chars
    global order_chars
    result = ''
    digit_count = 0
    while v != 0:
        if digit_count == 4 and order_codes:
            # Use the instruction order code in this column.
            result += order_chars[v % 16]
        else:
            result += hex_chars[v % 16]
        v /= 16
        min_digits -= 1
        digit_count += 1
    while min_digits > 0:
        result += '0'
        min_digits -= 1
    return result[::-1] # Reverse the string of digits.

'''
Convert a hexadecimal string into an integer value.
'''
def from_hex(s):
    global hex_chars
    global hex_chars_upper
    global order_chars
    global order_chars_upper
    result = 0
    for ch in s:
        try:
            digit = hex_chars.index(ch)
        except ValueError:
            try:
                digit = hex_chars_upper.index(ch)
            except ValueError:
                try:
                    digit = order_chars.index(ch)
                except ValueError:
                    digit = order_chars_upper.index(ch)
        result = (result << 4) + digit
    return result
