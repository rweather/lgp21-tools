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
