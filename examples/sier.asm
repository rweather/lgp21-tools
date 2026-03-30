;
; Sierpiński triangle for LGP-21.
;
    .entry  start
.1262:  start:          ld      newline
.1263:                  pr6
.1300:                  ld      size
.1301:                  st      y
;
.1302:  outer_loop:     ld      zero
.1303:                  jmp     print_sp_next
;
.1304:  print_spaces:   ld      space
.1305:                  pr6
.1306:                  ld      tmp
.1307:                  add     one
.1308:  print_sp_next:  st      tmp
.1309:                  sub     y
.1310:                  jn      print_spaces
;
.1311:                  ld      zero
.1312:                  st      x
.1313:                  ld      y
.1314:                  st      tmp
;
.1315:  print_points:   ld      x
.1316:                  and     y
.1317:                  sub     one
.1318:                  jn      print_point
.1319:                  ld      space
.1320:                  pr6
.1321:                  pr6
.1322:                  jmp     next_point
;
.1323:  print_point:    ld      show_point
.1324:                  pr6
.1325:                  shl6
.1326:                  pr6
;
.1327:  next_point:     ld      x
.1328:                  add     one
.1329:                  st      x
.1330:                  ld      tmp
.1331:                  add     one
.1332:                  st      tmp
.1333:                  sub     sizep1
.1334:                  jn      print_points
;
.1335:                  ld      newline
.1336:                  pr6
.1337:                  ld      y
.1338:                  sub     one
.1339:                  st      y
.1340:                  jn      done
.1341:                  jmp     outer_loop
;
.1342:  done:           hlt
;
.1343:  size:           .dw     #124     ; 31 * 4
.1344:  sizep1:         .dw     #128     ; (31 + 1) * 4
.1345:  show_point:     .dw     "+ "
.1346:  one:            .dw     0001
.1347:  zero:           .dw     0000
.1348:  space:          .dw     " "
.1349:  newline:        .dw     "\n"
    .noemit
.1350:  tmp:            .dw     0
.1351:  x:              .dw     0
.1352:  y:              .dw     0
