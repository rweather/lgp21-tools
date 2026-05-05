;
; Arithmetic test program for LGP-21 that resides in tracks 7 through 9.
;
; This program expects there to be a tape on the main tape reader that
; contains the test cases to execute.  Each test case consists of 5
; words terminated by a conditional stop:
;
;       a'1'2'1'n'3'    # Test 1 + 2 = 3
;
; The five words are:
;
;       Name of the instruction to execute.
;       Value to put in the accumulator (LSB can be 1).
;       Operand value to put in memory (LSB is ignored).
;       Value to put in the accumulator, again.
;       Expected overflow flag, either n for no overflow or v for overflow.
;       Expected result (LSB can be 1).
;
; The value to put in the accumulator is repeated because otherwise the
; accumulator's LSB would be lost if we tried to store it somewhere.
;
; The output will look like this:
;
;       a 00000001 00000002 00000003 n ?
;
; The columns are:
;
;       Name of the instruction.
;       Value of the accumulator before the instruction is executed.
;       Value of the memory operand.
;       Actual value computed by the LGP-21.
;       State of the overflow flag from the computation (n or v).
;       ? is printed if the result is wrong, nothing printed if result is ok.
;
; The tape should be terminated with a zero instruction:
;
;       0'
;
    .org    0700
    .entry  start
start:
;
; Print "ready" and wait for the user to enter a word before starting.
; This gives the user time to load the test case tape onto the reader.
;
    ld      newline
    pr6
    ld      ready
    pr6
    shl6
    pr6
    shl6
    pr6
    shl6
    pr6
    shl6
    pr6
    ld      zero
    in6
    ld      newline
    pr6
;
; Input the name of the instruction; e.g. "a'" or "m'".  Shift it into
; position and add the address of the operand word.
;
next_test:
    ld      zero
    in6     0000
    shl6
    shl4
    shl4
    st      inst_name
    and     inst_mask
    add     operand_addr
    st      doit
;
; Tests stop when we come across a zero instruction.
;
    sub     check_zero
    jn      tests_done
;
; Print the name of the instruction followed by a space.
;
    ld      inst_name
    shl6
    shl6
    pr6
    ld      space
    pr6
;
; Load the first operand, which will eventually go into A and print it.
; The act of printing will destroy the value, so we load it again later.
;
    ld      zero
    in4     0000
    sret    prhex_return
    jmp     prhex
;
; Load the second operand which will go into memory.  Strip the LSB and print.
;
    ld      zero
    in4     0000
    st      operand
    ld      operand
    sret    prhex_return
    jmp     prhex
;
; Reload the first value to put it into A again.
;
    ld      zero
    in4     0000
;
; Perform the instruction and print the result that ends up in A.
;
    -z      0200        ; Clear the overflow flag.
    nop
doit:
    add     operand     ; Replaced with the actual instruction to do.
    pr4
    st      result      ; Preserve bits 1..31 of the result.
    shl4
    st      result+1    ; Preserve bit 0 of the result, shifted up by 4 bits.
    sret    prhex_return
    jmp     prhex2
;
; Print the state of the overflow flag.
;
    ld      no_overflow
    -z      0200
    ld      overflow
    st      result+2
    pr6
    ld      space
    pr6
;
; Read the expected overflow flag from the tape: "n'" or "v'".
;
    ld      zero
    in6     0000
    shl6
    shl6
    shl6
    shl4
    shl4
    st      expected+1
;
; Read the expected result from the tape and check the actual result.
;
    ld      zero
    in4     0000
    st      expected    ; Preserve bits 1..31 of the expected value.
    shl4
    sub     result+1    ; Compare bit 0.
    jn      fail
    sub     two
    jn      check_high
fail:
    ld      question
    pr6
    shl6
    pr6
    shl6
    pr6
    jmp     end_test
check_high:
    ld      expected    ; Compare bits 1..31.
    sub     result
    jn      fail
    sub     two
    jn      check_overflow
    jmp     fail
;
; Check that the overflow flag is as expected.
;
check_overflow:
    ld      expected+1
    sub     result+2
    jn      fail
    sub     two
    jn      end_test
    jmp     fail
;
; Print a newline and go back for the next test case
;
end_test:
    ld      newline
    pr6
    jmp     next_test
;
tests_done:
    hlt
;
; Print a hexadecimal word followed by a space.
;
prhex:
    pr4
    shl4
prhex2:
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
    shl4
    pr4
    ld      space
    pr6
prhex_return:
    jmp     0
;
; Constants.
;
ready:
    .dw     "ready"
newline:
    .dw     "\n"
space:
    .dw     " "
question:
    .dw     "?"
overflow:
    .dw     $7c000000   ; "v" followed by NUL's
no_overflow:
    .dw     $64000000   ; "n" followed by NUL's
operand_addr:
    .dw     operand
zero:
    .dw     0
two:
    .dw     #2
inst_mask:
    .dw     $000F0000
check_zero:
    .dw     operand+1
;
; Variables.
;
    .noemit
operand:
    .dw     0
inst_name:
    .dw     0
result:
    .dw     0, 0, 0
expected:
    .dw     0, 0
