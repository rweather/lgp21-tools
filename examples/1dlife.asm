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
; The program needs 5 tracks of space on the magnetic disk for the
; code and the state of the game board.
;
    .org    1500
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
    ld      addr_of_board
    st      posn
    ld      addr_of_board2
    sta     count_store
count_loop:
    ld      posn
;
; Count the neighbors of the cell at the address in A.  The count is left
; in the variable "ncount" and the state of the current cell is left in A.
;
    sub     inc_addr
    sta     count_nb1
    sub     inc_addr
    sta     count_nb2
    add     three_addr
    sta     count_nb3
    add     inc_addr
    sta     count_nb4
count_nb1:
    ld      0000
count_nb2:
    add     0000
count_nb3:
    add     0000
count_nb4:
    add     0000
count_store:
    st      0000            ; Store the cell count to the "board2" array.
;
    ld      count_store     ; Advance to the next cell to count.
    add     inc_addr
    sta     count_store
    ld      posn
    add     inc_addr
    st      posn
    sub     board_end
    jn      count_loop
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
    st      compute_prev_dead
    st      compute_prev_alive
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
