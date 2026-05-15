;
; 1-D version of Conway's Game of Life
;
; https://jonmillen.com/1dlife/index.html
;
; In a five-cell arrangment YYXYY, the following rules apply:
; - A cell is born if it has 2 or 3 Y neighbors alive.
; - A living cell survives if it has 2 or 4 Y neighbors.
;
; The game board in this version is 64 cells wide.
;
; The program needs 9 tracks of space on the magnetic disk for the
; code and the state of the game board.
;
    .org    5000
    .entry  start
start:
;
    ld      newline
    pr6
;
    sret    gen_random_return
    jmp     gen_random
;
    ld      counter_init
    st      counter
;
loop:
    sret    gen_print_return
    jmp     gen_print
;
    sret    compute_return
    jmp     compute
;
    ld      counter             ; Have we finished all generations yet?
    add     inc_addr
    st      counter
    jn      loop                ; No, go back for more.
;
    ld      newline
    pr6
    hlt                         ; Done!
;
; Compute the next generation of cells.
;
compute:
    ld      board+1
    add     board+2
    st      board2
    ld      board
    add     board+2
    add     board+3
    st      board2+1
    ld      board
    add     board+1
    add     board+3
    add     board+4
    st      board2+2
    ld      board+1
    add     board+2
    add     board+4
    add     board+5
    st      board2+3
    ld      board+2
    add     board+3
    add     board+5
    add     board+6
    st      board2+4
    ld      board+3
    add     board+4
    add     board+6
    add     board+7
    st      board2+5
    ld      board+4
    add     board+5
    add     board+7
    add     board+8
    st      board2+6
    ld      board+5
    add     board+6
    add     board+8
    add     board+9
    st      board2+7
    ld      board+6
    add     board+7
    add     board+9
    add     board+10
    st      board2+8
    ld      board+7
    add     board+8
    add     board+10
    add     board+11
    st      board2+9
    ld      board+8
    add     board+9
    add     board+11
    add     board+12
    st      board2+10
    ld      board+9
    add     board+10
    add     board+12
    add     board+13
    st      board2+11
    ld      board+10
    add     board+11
    add     board+13
    add     board+14
    st      board2+12
    ld      board+11
    add     board+12
    add     board+14
    add     board+15
    st      board2+13
    ld      board+12
    add     board+13
    add     board+15
    add     board+16
    st      board2+14
    ld      board+13
    add     board+14
    add     board+16
    add     board+17
    st      board2+15
    ld      board+14
    add     board+15
    add     board+17
    add     board+18
    st      board2+16
    ld      board+15
    add     board+16
    add     board+18
    add     board+19
    st      board2+17
    ld      board+16
    add     board+17
    add     board+19
    add     board+20
    st      board2+18
    ld      board+17
    add     board+18
    add     board+20
    add     board+21
    st      board2+19
    ld      board+18
    add     board+19
    add     board+21
    add     board+22
    st      board2+20
    ld      board+19
    add     board+20
    add     board+22
    add     board+23
    st      board2+21
    ld      board+20
    add     board+21
    add     board+23
    add     board+24
    st      board2+22
    ld      board+21
    add     board+22
    add     board+24
    add     board+25
    st      board2+23
    ld      board+22
    add     board+23
    add     board+25
    add     board+26
    st      board2+24
    ld      board+23
    add     board+24
    add     board+26
    add     board+27
    st      board2+25
    ld      board+24
    add     board+25
    add     board+27
    add     board+28
    st      board2+26
    ld      board+25
    add     board+26
    add     board+28
    add     board+29
    st      board2+27
    ld      board+26
    add     board+27
    add     board+29
    add     board+30
    st      board2+28
    ld      board+27
    add     board+28
    add     board+30
    add     board+31
    st      board2+29
    ld      board+28
    add     board+29
    add     board+31
    add     board+32
    st      board2+30
    ld      board+29
    add     board+30
    add     board+32
    add     board+33
    st      board2+31
    ld      board+30
    add     board+31
    add     board+33
    add     board+34
    st      board2+32
    ld      board+31
    add     board+32
    add     board+34
    add     board+35
    st      board2+33
    ld      board+32
    add     board+33
    add     board+35
    add     board+36
    st      board2+34
    ld      board+33
    add     board+34
    add     board+36
    add     board+37
    st      board2+35
    ld      board+34
    add     board+35
    add     board+37
    add     board+38
    st      board2+36
    ld      board+35
    add     board+36
    add     board+38
    add     board+39
    st      board2+37
    ld      board+36
    add     board+37
    add     board+39
    add     board+40
    st      board2+38
    ld      board+37
    add     board+38
    add     board+40
    add     board+41
    st      board2+39
    ld      board+38
    add     board+39
    add     board+41
    add     board+42
    st      board2+40
    ld      board+39
    add     board+40
    add     board+42
    add     board+43
    st      board2+41
    ld      board+40
    add     board+41
    add     board+43
    add     board+44
    st      board2+42
    ld      board+41
    add     board+42
    add     board+44
    add     board+45
    st      board2+43
    ld      board+42
    add     board+43
    add     board+45
    add     board+46
    st      board2+44
    ld      board+43
    add     board+44
    add     board+46
    add     board+47
    st      board2+45
    ld      board+44
    add     board+45
    add     board+47
    add     board+48
    st      board2+46
    ld      board+45
    add     board+46
    add     board+48
    add     board+49
    st      board2+47
    ld      board+46
    add     board+47
    add     board+49
    add     board+50
    st      board2+48
    ld      board+47
    add     board+48
    add     board+50
    add     board+51
    st      board2+49
    ld      board+48
    add     board+49
    add     board+51
    add     board+52
    st      board2+50
    ld      board+49
    add     board+50
    add     board+52
    add     board+53
    st      board2+51
    ld      board+50
    add     board+51
    add     board+53
    add     board+54
    st      board2+52
    ld      board+51
    add     board+52
    add     board+54
    add     board+55
    st      board2+53
    ld      board+52
    add     board+53
    add     board+55
    add     board+56
    st      board2+54
    ld      board+53
    add     board+54
    add     board+56
    add     board+57
    st      board2+55
    ld      board+54
    add     board+55
    add     board+57
    add     board+58
    st      board2+56
    ld      board+55
    add     board+56
    add     board+58
    add     board+59
    st      board2+57
    ld      board+56
    add     board+57
    add     board+59
    add     board+60
    st      board2+58
    ld      board+57
    add     board+58
    add     board+60
    add     board+61
    st      board2+59
    ld      board+58
    add     board+59
    add     board+61
    add     board+62
    st      board2+60
    ld      board+59
    add     board+60
    add     board+62
    add     board+63
    st      board2+61
    ld      board+60
    add     board+61
    add     board+63
    st      board2+62
    ld      board+61
    add     board+62
    st      board2+63
;
; Iterate over "board" and "board2" to figure out which cells are
; alive and dead in the next generation.
;
    ld      addr_of_board
    sta     compute_loop
    sta     compute_store
    ld      addr_of_board2
    sta     compute_prev_dead
    sta     compute_prev_alive
;
; Was the previous cell alive or dead?
;
compute_loop:
    ld      0000
    shl4
    jn      compute_prev_alive
;
; Previously the cell was dead.  Comes alive if 2 or 3 neighbors.
;
compute_prev_dead:
    ld      0000
    sub     twice_live_cell
    jn      new_cell_dead
    sub     twice_live_cell
    jn      new_cell_alive
new_cell_dead:
    ld      zero
    jmp     compute_store
;
; Previously the cell was alive.  Cell dies with 0, 1, or 3 neighbors.
;
compute_prev_alive:
    ld      0000
    sub     twice_live_cell
    jn      new_cell_dead
    sub     live_cell
    jn      new_cell_alive
    sub     live_cell
    jn      new_cell_dead
new_cell_alive:
    ld      live_cell
;
compute_store:
    st      0000
    ld      compute_prev_dead
    add     inc_addr
    sta     compute_prev_dead
    sta     compute_prev_alive
    ld      compute_loop
    add     inc_addr
    sta     compute_loop
    sta     compute_store
    sub     end_board_load
    jn      compute_loop
compute_return:
    jmp     0000
;
; Generate random data into the game board.  Only the "live_cell"
; bit of each word matters, indicating whether a cell is alive or dead.
;
gen_random:
    ld      addr_of_board
    sta     gen_word
gen_next:
    sret    rand_return
    jmp     rand
    and     live_cell       ; AND off the bit we care about only.
gen_word:
    st      0000
    ld      gen_word
    add     inc_addr
    sta     gen_word
    sub     end_board_store
    jn      gen_next
    ld      zero            ; Set boundary cells to zero.
    st      board-0002
    st      board-0001
    st      board+0100
    st      board+0101
gen_random_return:
    jmp     0000
;
; Print a single generation on a line of its own.
;
gen_print:
    ld      shift_upper     ; Print the "shift to upper case" code.
    pr6
;
    ld      addr_of_board
    sta     gen_print_word
gen_print_word:
    ld      0000
    shl4
    jn      gen_print_alive
    ld      cell_dead
    jmp     gen_print_next
gen_print_alive:
    ld      cell_alive
gen_print_next:
    pr6
;
    ld      gen_print_word
    add     inc_addr
    sta     gen_print_word
    sub     end_board_load
    jn      gen_print_word
;
    ld      shift_lower     ; Print the "shift to lower case" code.
    pr6
    ld      newline         ; Terminate the line.
    pr6
gen_print_return:
    jmp     0000
;
; Constants.
;
zero:
    .dw     0
live_cell:
    .dw     $08000000       ; Value that is used for a live cell.
twice_live_cell:
    .dw     $10000000       ; 2 * live_cell
shift_upper:
    .dw     $20000000       ; Character that shifts to upper case.
shift_lower:
    .dw     $10000000       ; Character that shifts to lower case.
cell_dead:
    .dw     " "
cell_alive:
    .dw     $28000000       ; "*" without shift codes.
newline:
    .dw     "\n"
addr_of_board:
    .dw     board
addr_of_board2:
    .dw     board2
inc_addr:
    .dw     0001
two_addr:
    .dw     0002
three_addr:
    .dw     0003
board_end:
    .dw     board+0100
end_board_store:
    st      board+0100
end_board_load:
    ld      board+0100
counter_init:
    .dw     #-100           ; 25 * 4 for 25 generations.
;
; Include the random number generation routines.
;
    .include random.asm
;
; Variables.
;
    .noemit
counter:
    .dw     0               ; Generation counter.
posn:
    .dw     0               ; Position in "board" when computing new generation.
;
; Storage for the game board.  There are two extra words before the
; board and two extra words after the board containing zeroes.
; This makes it easier to count neighbors of the boundary cells.
; Total of 64 + 4 = 68 words are needed to store the game board.
;
    .dw     0, 0
board:
;
; New version of the board after computing the next generation.
;
    .org    board+0102
board2:
