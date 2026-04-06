LGP-21 Assembler Syntax
=======================

The `lgp21-assembler` program converts LGP-21 assembly code into
tape images that can be loaded onto a LGP-21 device.  The syntax
reflects modern assembly code conventions to make the modern
LGP-21 programmer's job easier.

## Using the assembler

Simplest is to run the assembler on the `.asm` file to generate a `.txt`
tape image:

    lgp21-assembler output.txt input.asm

If you wish to generate a binary `.ptp` image which is ready to punch on
paper tape, use the `-b` or `--binary` option:

    lgp21-assembler -b output.ptp input.asm

Other options:

* `-r` or `--relocatable` generates a relocatable image (experimental,
not completely working yet).
* `-w NUM` or `--word-per-line NUM` sets the number of words per line
in the resulting tape image; defaults to 8.
* `-B` or `--bootstrap` generates bootstrap code to load the tape without PIR.
The bootstrap occupies 15 words of memory at the bootstrap start address.
* `-C` or `--compact-bootstrap` generates compact bootstrap code to load the
tape without PIR.  The bootstrap occupies 5 words of memory at the bootstrap
start address.
* `-A ADDR` or `--bootstrap-address ADDR` sets the bootstrap start address;
defaults to 6300.
* `-D DEV` or `--boostrap-device DEV` sets the bootstrap device; 0 for the
tape reader and 2 for the Flexowriter.  The default is 2.
* `-L LISTFILE` or `--listing LISTFILE` specifies the listing output file.
By default, no listing is generated.

## Case sensitivity

Labels and directive names are case-sensitive.  Instruction names are
not case-sensitive.

## Lines

Each line consists of an optional label and an instruction, or the line
is a directive starting with a period (.).  Comments start with a
semi-colon (;) and extend to the end of the line.  Blank lines or
lines with a comment only are ignored.  Some exmamples:

    label:                  ; Label on a line of its own

    label: p 0200           ; Label followed by an instruction

    label:                  ; Label with the instruction on the next line
        p 0200

    label = 42              ; Assign a value to a label symbol

    .org 0300               ; Change the origin address to 0300

## Manual placement

Manual placement of instructions and data can help optimize for the
LGP-21's disk rotation.  This can be done with `.org`:

      .org 0300
      b msg
      .org 0301
      p 0200
      i 6200
      ...
      .org 0436
    msg:
      w "Hi there"

This can get very tedious, so it is also possible to prefix instructions
with the address directly:

    .0300: b msg
    .0301: p 0200
           i 6300
    ...
    .0436: msg:
           w "hello"

If an address is not specified, it will automatically increment from the
previous line.

## Addresses and numbers

Addresses are specified in "LGP-21 decimal" which is not the same as
regular decimal.  The four digits are split into two-digit track and
sector values, each between 00 and 63.  The following are valid addresses:

    0100        ; Sector 0 of track 1
    6304        ; Sector 4 of track 63
    12          ; Sector 12 of track 0

An error will be raised if the track or sector numbers are out of range.

To use a regular decimal constant in the code, prefix it with "#":

    #0100       ; The decimal number 100
    #42         ; The decimal number 42
    #-741       ; The decimal number -741 in two's complement form

Hexadecimal numbers may be prefixed with "$" for regular 0-9a-f hexadecimal,
or with "&" for "LGP-21 hexadecimal" which uses 0-9fgjkqw.  The following
two values are the same constant:

    $c651f68a
    &j651w68f

Either upper or lower case hexadecimal characters are allowed.

Floating-point values -1.0 <= n < 1.0 may be written directly as long
as they contain a decimal point:

    -1.
    -0.987654
    -0.5
    0.
    0.5
    0.987654
    0.9999999999

The value is scaled by 2^31 to convert it into a LGP-21 word.

To facilitate scaling of constants, loating point values may also include
a right shift:

    3.1415 >> 4

The value is first shifted to the right by N bits, and then stored. The
result after the shift must be in the range -1.0 <= n < 1.0. See section
5 of the LGP-21 Programming Manual for information on scaled fixed point
arithmetic.

Note: When a word value is stored in a memory location, the least significant
bit is lost and set to zero when the word is reloaded.  The accumulator
can store a full 32 bits, although some operations like multiplication and
division will lose the least significant bit in the result.

## Labels

Labels start with any of A-Z, a-z, or underscore.  The rest of the name
may be any of 0-9, A-Z, a-z, or underscore.

Labels may be bound to a specific location in the program by writing them
in the left-most column with a colon (:) like so:

    start:
    msg:

The exception to this is when an explicit address is supplied:

    .0300: start:
    .0426: msg:

Labels may be defined to a specific value using variable assignment:

    pi_on_4 = 0.7853981634
    meaning_of_life = #42
    scratch_memory = 2400   ; Memory address, track 24, sector 0

## Expressions

The address operand to an instruction can use addition and subtraction of a
constant to modify the value by a decimal amount:

    b msg       ; Retrieve the first word of msg
    b msg+1     ; Retrieve the second word of msg
    h x - 10    ; Store A to 10 memory locations before x

The special symbol `*` refers to the current address in the program:

    u *         ; Infinite loop: jump back to this instruction over and over
    b *+3       ; Load A from 3 words on from this instruction

These are presently the only forms of expressions that are supported.

## Directives

`.org ADDRESS` changes the origin to the new `ADDRESS`.

`.entry ADDRESS` causes the resulting tape to auto-execute the code
starting from `ADDRESS` after the program is loaded from tape.

`.dw VALUE` causes literal word values to be written into the program:

    .dw #42
    .dw #1, #2, 0300, $c651f68a, 0.7853981634
    .dw "HELLORLD"
    .dw 'GOODBYE\n'

Strings are encoded in 6-bit character codes, with up to 5 per word.
Left-over bits will be padded on the right with zero bits.  The escape
sequences "\"", "\'", "\n", "\b", and "\t" may be used for quotes, newline,
backspace, and tab but no other escape sequences are recognised.

It is assumed that the character set for a string starts in lower case.
Shift codes are inserted to switch to and from upper case as necessary.
The character set will revert to lower case at the end of the string.
The "HELLORLD" string from the example above expands to 12 character
codes (or 3 words), including the shift to upper case at the start of the
string, and the shift to lower case at the end of the string.

`.noemit` reserves space for the declarations that follow but does not
emit them into the final tape image.  This can be used to reserve space
for variables.  `.emit` returns to normal operation.

`.include FILENAME` includes another source file at this location in the
parent.  The `FILENAME` is interpreted relative to the including file.
Does not check for recursive includes; it keeps including forever.

## Instructions

Instruction names may be in either upper or lower case.  Instruction
generally have the form "OPCODE ADDRESS".  Some friendly aliases are
provided for convenience.

<table border="1">
<tr><td><b>Opcode</b></td><td><b>Aliases</b></td><td><b>Description</b></td></tr>
<tr><td><tt>a</tt></td><td><tt>add</tt></td><td>Adds the value at the address to the accumulator.</td></tr>
<tr><td><tt>b</tt></td><td><tt>ld</tt></td><td>Brings (or loads) the value at the address into the accumulator.</td></tr>
<tr><td><tt>c</tt></td><td><tt>stc</tt> or <tt>clr</tt><td>Stores the value in the accumulator at the address, and then clears the accumulator.</td></tr>
<tr><td><tt>d</tt></td><td><tt>div</tt><td>Divides the accumulator by the value at the address.</td></tr>
<tr><td><tt>e</tt></td><td><tt>and</tt></td><td>Bitwise AND of the accumulator with the value at the address.</td></tr>
<tr><td><tt>h</tt></td><td><tt>st</tt></td><td>Holds (or stores) the value in the accumulator at the address.</td></tr>
<tr><td><tt>i</tt></td><td><tt>in6</tt> or <tt>shl6</tt></td><td>Input 6-bit values into the accumulator, or shift the accumulator left by 6 bits if the address is 6200.  The address is the device number.</td></tr>
<tr><td><tt>-i</tt></td><td><tt>in4</tt> or <tt>shl4</tt></td><td>Input 4-bit values into the accumulator, or shift the accumulator left by 4 bits if the address is 6200.  The address is the device number.</td></tr>
<tr><td><tt>m</tt></td><td><tt><tt>mulh</tt></td><td>Multiplies the accumulator by the value at the address and returns the high 31 bits in the accumulator.</td></tr>
<tr><td><tt>n</tt></td><td><tt>mull</tt></td><td>Multiplies the accumulator by the value at the address and returns the low 31 bits in the accumulator.</td></tr>
<tr><td><tt>p</tt></td><td><tt>pr6</tt></td><td>Prints the top 6 bits of the accumulator to the device number in the address field.</td></tr>
<tr><td><tt>-p</tt></td><td><tt>pr4</tt></td><td>Prints the top 4 bits of the accumulator as a hexadecimal character to the device number in the address field.</td></tr>
<tr><td><tt>r</tt></td><td><tt>sret</tt></td><td>Store the address of PC+2 to the address bits of the memory location, preserving all other bits at the destination.</td></tr>
<tr><td><tt>s</tt></td><td><tt>sub</tt></td><td>Subtracts the value at the address from the accumulator.</td></tr>
<tr><td><tt>t</tt></td><td><tt>jn</tt></td><td>Conditional jump to the address if the accumulator is negative.</td></tr>
<tr><td><tt>-t</tt></td><td><tt>jnt</tt></td><td>Conditional jump to the address if the accumulator is negative or the TC switch is set.</td></tr>
<tr><td><tt>u</tt></td><td><tt>jmp</tt></td><td>Unconditional jump to the address.</td></tr>
<tr><td><tt>y</tt></td><td><tt>sta</tt></td><td>Store the address bits of the accumulator to the address bits of the memory location, preserving all other bits at the destination.</td></tr>
<tr><td><tt>z</tt></td><td><tt>hlt</tt> or <tt>nop</tt></td><td>Halt the machine or not based on a condition given by the address.</td></tr>
<tr><td><tt>-z</tt></td><td><tt>ovr</tt></td><td>Halt the machine or skip the next instruction based on a condition given by the address and the overflow flag.</td></tr>
</table>

The aliases "hlt", "nop", "shl4", and "shl6" do not have an operand
as the address value is implicit.

The operand to "in4", "in6", "pr4", "pr6" can be omitted to default to the
typewriter, device 0200.

Consult the [LGP-21 Programming Manual](https://bitsavers.org/pdf/generalPrecision/LGP-21/LGP-21_Programming_Manual_1963.pdf)
for more information on the opcodes and their operands.

## Example

The following program prints the Fibonacci sequence in hexadecimal.
Stops when the word in A overflows and becomes negative.

        .org 1000
        .entry start
    start:
        ld  one
        clr var1        ; Set var1 to 1.
        st  var2        ; Set var2 to 0.
        ld  var1        ; Preload var1 into A.
    ;
    ; The loop ping-pongs between the two working variables.
    ;
    loop:
        sret print_end  ; Call the "print" subroutine for the first value.
        jmp print
        ld  var1        ; Compute a new second value.
        add var2
        jn  finish
        st  var2
        sret print_end  ; Call the "print" subroutine for the second value.
        jmp print
        ld  var2        ; Compute a new first value.
        add var1
        jn  finish
        st  var1
        jmp loop        ; Go back for more.
    finish:
        hlt             ; Stop when the word overflows.
    print:
        pr4             ; Print the 7 hexadecimal digits of the value in A.
        shl4
        pr4
        shl4
        pr4
        shl4
        pr4
        shl4
        pr4
        shl4
        pr4
        shl4
        pr4
        ld  eol         ; Print a newline.
        pr6
    print_end:
        jmp 0000        ; Return back to the caller.
    one:
        .dw #16         ; Shifted up by 4 bits because the LSB is unusable.
    eol:
        .dw "\n"
    ;
    ; Reserve space for the variables.
    ;
        .noemit
    var1:
        .dw 0
    var2:
        .dw 0
