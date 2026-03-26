;
; Example that prints "he11o1rd" over and over.
;
    .org 1000
    .entry start
start:
    b msg           ; Bring first word of message into A.
    p 0200          ; Print top 6 bits of A to the typewriter.
    i 6200          ; Shift A left by 6 bits.
    p 0200          ; Repeat for 4 more characters.
    i 6200
    p 0200
    i 6200
    p 0200
    i 6200
    p 0200
    b msg+1         ; Bring second word of message into A.
    p 0200          ; Print 3 characters out of the second word.
    i 6200
    p 0200
    i 6200
    p 0200
    i 6200
    p 0200
    u start
msg:
    .dw &j651868j   ; Literal words for the message in hexadecimal.
    .dw &34655000
