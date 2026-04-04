Using the Program Input Routine
================================

The Program Input Routine is described in the [LGP-30 Subroutine
Manual](https://www.bitsavers.org/pdf/generalPrecision/LGP-30/LGP-30_Subroutine_Manual_Aug57.pdf).
It is assumed that the LGP-21 PIR operates the same way, and evidence
so far supports this.

The PIR allows instructions and hexadecimal data to be entered into
memory, and provides a means for the immediate execution of
instructions.

The PIR supports loading relocatable code by allowing you to specify a
**modifier** value that is added to the address field of each
instruction as it is entered.

Data entry begins by specifying the destination address using the
**Start Fill** command. The first word will be placed at that address,
with the address automatically incrementing as subsequent words are
entered.

# PIR Commands

## `+` Execute Instruction Immediately

Loads an instruction into the instruction register and a value into the
accumulator, then executes the instruction immediately.

* Example: `+00p0200'55555555'` loads a P (print) instruction, loads
  `55555555` into A, and executes it, printing the top 6 bits from A
  as the letter `d`.
* Example: `+00u0f00''` loads `U 1000` (an unconditional jump to
  address `1000`) into the instruction register, loads zero into A,
  and executes it.

## `;` Start Fill

Sets the starting address at which subsequent data will be loaded.

* Example: `;0001000'` — subsequent data will be loaded starting at
  address `1000`.

## `/` Set Modifier

Sets the modifier value. The address field of each instruction loaded
after this point will have the modifier added to it.

* Example: `/0000000'` — do not modify any address field.
* Example: `/0000100'` — add `100` to every subsequent instruction's
  address field.

**Prefix an instruction with `x` to suppress the modifier for that
instruction only.**

## Instruction

Instructions are entered directly using their mnemonics, with no
prefix.

* Example: `b 1234'`
* Example: `i 6300'`

To prevent the modifier from being applied to an instruction's address
field, prefix it with `x`.

* Example: `x u 1000'`

## `,` Hex Words

Enters one or more hexadecimal words. The `,` command takes the number
of words to follow, and then that many hex words are entered in
sequence. Leading zeros may be omitted.

* Example: `,00000004' 1' 22' ' 42'` — enters the four words `1`,
  `22`, `0`, and `42`.

## `m` Hex Block and Checksum

The `m` command introduces a block of hexadecimal words.  The following
is an example:

    m40k0001'f0591'30195'f01g5'g036k'1024k'202f5'400'
    f02q5'f02jk'10445'g00w1'q0485'80200'80200'j041k'
    90479'w047k'g020k'w04w5'g0231'f021k'1041k'80200'
    10425'q0445'43q00'43q00'80200'903j9'50421'300qk'
    f00j5'103w5'80200'1000'40'800'f0001'30261'
    f026k'g0005'f0391'80080200'80043q00'f0241'2017k'f0251'
    1075k'50419'80080200'904q9'60341'80080200'90411'503wk'
    80080200'90401'60341'80080200'f0001'80080200'q0415'80200'
    f0039'w5q276q9'

The first word is the block header and specifies the length of the block
and the starting address.  For example:

    m40k0001

    m       Instruction name
    40      Block length N, 0x40 = 64 decimal
    k       Opcode for a CLEAR instruction
    0001    Starting address with the LSB set

The header word is followed by the N data words of the block, and then the
checksum word.

If a data word has the LSB set, then it indicates that data word should be
relocated using the `/` modifier.  Otherwise the data word is used as-is.

The checksum word is the sum of the header word and the N words of the block,
ignoring the LSB in each of the words.

## `.` Stop and Transfer

The `.` command stops the machine and prepares to start executing code at
the address in the command word.  If the BS32 switch is set, execution
starts immediately.  Otherwise the machine halts and waits for the user
to press START.

The following command starts executing code at track 10, sector 0.

    .0001000'

# Full Example

The following example prints 'hellorld' repeatedly.

Note that all addresses are relative to the first instruction `u0003`. This example loads the program at address 1000, and modifies instruction addresses by adding 1000.
The address and modifier in the first line may be changed to load it to a different location.

The 'p' Print and 'i' Shift instructions' address fields refer to IO devices, not memory locations, and so they are prefixed with an 'x' so that they are not modified.

```
;0001000'/0001000'      Begin loading data at address 1000 with 1000 as modifier
u0003'                  Unconditional transfer to 0003 (Modified to 1003)
,0000002'               Enter 2 hex words:
j651868j'                   First word
34655000'                   Second word
b0001'                  Load 0001 → A (Modified to 1001)
xp0200' xi6200'         6-bit print; shift A left 6 bits
xp0200' xi6200'
xp0200' xi6200'
xp0200' xi6200'
xp0200' xi6200'
b0002'                  Load 0002 → A (Modified to 1002)
xp0200' xi6200'
xp0200' xi6200'
xp0200' xi6200'
xp0200' xi6200'
u0000'                  Unconditional transfer to 0000 (Modified to 1000)


+00u0f00''              Tell PIR to Execute: U 1000 immediately
```
