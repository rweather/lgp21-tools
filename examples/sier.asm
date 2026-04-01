;
; Sierpiński triangle for LGP-21.
;
    .entry  start
.1300:  start:          ld      newline
.1301:                  pr6
.1302:                  shl6
.1303:                  pr6
.1304:                  ld      size
.1305:                  st      y
;
.1306:  outer_loop:     ld      zero
.1307:                  jmp     print_sp_next
;
.1308:  print_spaces:   ld      space
.1309:                  pr6
.1310:                  ld      tmp
.1311:                  add     one
.1312:  print_sp_next:  st      tmp
.1313:                  sub     y
.1314:                  jn      print_spaces
;
.1315:                  ld      zero
.1316:                  st      x
.1317:                  ld      y
.1318:                  st      tmp
;
.1319:  print_points:   ld      x
.1320:                  and     y
.1321:                  sub     one
.1322:                  jn      print_point
.1323:                  ld      space
.1324:                  pr6
.1325:                  pr6
.1326:                  jmp     next_point
;
.1327:  print_point:    ld      show_point
.1328:                  pr6
.1329:                  shl6
.1330:                  pr6
;
.1331:  next_point:     ld      x
.1332:                  add     one
.1333:                  st      x
.1334:                  ld      tmp
.1335:                  add     one
.1336:                  st      tmp
.1337:                  sub     sizep1
.1338:                  jn      print_points
;
.1339:                  ld      newline
.1340:                  pr6
.1341:                  shl6
.1342:                  pr6
.1343:                  ld      y
.1344:                  sub     one
.1345:                  st      y
.1346:                  jn      done
.1347:                  jmp     outer_loop
;
.1349:  done:           ld      shift_lower ; End in lower case.
.1350:                  pr6
.1351:                  hlt
;
.1352:  sizep1:         .dw     #128     ; (31 + 1) * 4
.1353:  size:           .dw     #124     ; 31 * 4
.1354:  newline:        .dw     "\nX"    ; Newline followed by shift to upper.
.1355:  shift_lower:    .dw     $10000000
.1356:  show_point:     .dw     "4 "     ; "Delta" in the upper case alphabet.
.1357:  one:            .dw     0001
.1358:  zero:           .dw     0000
.1359:  space:          .dw     " "
    .noemit
.1362:  x:              .dw     0
.1363:  y:              .dw     0
.1401:  tmp:            .dw     0
