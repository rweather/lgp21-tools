;
; Example that prints negative-terminated strings with a subroutine.
;
    .org 1100
    .entry start
start:
    ld      msg1_addr
    sret    prstr_return
    jmp     prstr
    ld      msg2_addr
    sret    prstr_return
    jmp     prstr
    hlt
;
prstr:
    sta     prstr_load
prstr_load:
    ld      0000
    pr6
    shl6
    pr6
    shl6
    pr6
    shl6
    pr6
    shl6
    pr6
    shl6
    jn      prstr_return
    ld      prstr_load
    add     inc_addr
    sta     prstr_load
    jmp     prstr_load
prstr_return:
    jmp     0000
;
inc_addr:
    .dw     0001
msg1_addr:
    .dw     msg1
msg1:
    .dw     "\nHello, World\n"
msg2_addr:
    .dw     msg2
msg2:
    .dw     "Goodbye, World\n"
