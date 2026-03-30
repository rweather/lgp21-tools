;
; Sierpiński triangle for LGP-21.
;
    .org    1300
    .entry  start
start:
    ld      size
    st      y
;
outer_loop:
    ld      zero
    st      tmp
;
print_spaces:
    ld      space
    pr6
    ld      tmp
    add     one
    st      tmp
    sub     y
    jn      print_spaces
;
    ld      zero
    st      x
    ld      y
    st      tmp
;
print_points:
    ld      x
    and     y
    sub     one
    jn      print_point
    ld      space
    pr6
    pr6
    jmp     next_point
;
print_point:
    ld      show_point
    pr6
    shl6
    pr6
;
next_point:
    ld      x
    add     one
    st      x
    ld      tmp
    add     one
    st      tmp
    sub     sizep1
    jn      print_points
;
    ld      newline
    pr6
    ld      y
    sub     one
    st      y
    jn      done
    jmp     outer_loop
done:
    hlt

size:
    .dw     #124     ; 31 * 4
sizep1:
    .dw     #128     ; (31 + 1) * 4
zero:
    .dw     0
one:
    .dw     0001
show_point:
    .dw     "+ "
space:
    .dw     " "
newline:
    .dw     "\n"
    .noemit
x:
    .dw     0
y:
    .dw     0
tmp:
    .dw     0
