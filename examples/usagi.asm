;
; Example that prints a Usagi.
;
    .org 4000
    .entry start
start:
    ld      usagi_addr
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
    hlt
;
inc_addr:
    .dw     0001
usagi_addr:
    .dw     usagi
usagi:
    .dw &4100j30j, &0j30j30j, &0j38f20j, &0j30j30j, &0j30j30j, &0j30j30j
    .dw &0j30j30j, &0q28900j, &0j30j30j, &0j30q288, &8f20j30j, &0j30j30j
    .dw &0j30j30j, &0j30j30j, &0j38f288, &8900j30j, &0j30j388, &8f221610
    .dw &5q28f21j, &0j30j30j, &0j30j30j, &0j30j30j, &8f28f25j, &8f288740
    .dw &0j30j30j, &8f25k75j, &5k75k75j, &5q20j30j, &0j30j30j, &0j30j388
    .dw &8975k75j, &5k75k75j, &8f24030j, &0j30q25j, &5k75k720, &2j45k75j
    .dw &5q28830j, &0j30j30j, &0j30j388, &5k75k75j, &20g1175j, &5k78f240
    .dw &0j30j30j, &8975k72j, &8882j45j, &5k75q288, &0j30j30j, &0j30j30j
    .dw &0q25k75j, &20w1222j, &5k75k788, &8900j30j, &0j38975j, &5k720w2j
    .dw &11788g5j, &8f20j30j, &0j30j30j, &0j30q25j, &5k75k720, &2j45q288
    .dw &5q28900j, &0j30j388, &5k75q288, &20g1175j, &5k78f20j, &0j30j30j
    .dw &0j30j30j, &8975k788, &8882j45j, &5k75q288, &4030j30j, &0q25k75j
    .dw &5j83jg10, &8f25k788, &8830j30j, &0j30j30j, &0j38975j, &5k75j82j
    .dw &7848975j, &8f24030j, &0j30q25j, &5k78f220, &2j45k75j, &5q28830j
    .dw &0j30j30j, &0j30j388, &5k75q288, &20g1175j, &5k78f240, &0j30j30j
    .dw &8975k75j, &20w2j488, &8975q288, &0j30j30j, &0j30j30j, &0q25k75j
    .dw &5k720g10, &8f25k788, &8900j30j, &0j38975j, &5q220f2j, &1175k75j
    .dw &8f20j30j, &0j30j30j, &0j30q25j, &5k78f220, &2j45k75j, &5q28900j
    .dw &0j30j388, &5k75k720, &3jg12288, &5k78f20j, &0j30j30j, &0j30j30j
    .dw &8975k75j, &5j82j488, &8975q288, &4030j30j, &0q25k788, &89720g10
    .dw &5k75k788, &8830j30j, &0j30j30j, &0j38975j, &21q1225j, &20g1175j
    .dw &5k78f240, &0j30j30j, &8975k75j, &20w78488, &5k75q288, &0j30j32j
    .dw &2j70j30j, &0q25k75j, &5k720g10, &8882j45j, &5q28900j, &0j30j388
    .dw &5k72jg1j, &20g10g2j, &2k78f22j, &5k75k75j, &5k75k788, &8975jg2j
    .dw &2j82j42j, &2jg5q288, &4030j30j, &0q25k75j, &5k720g10, &5k75k75j
    .dw &5k75k75j, &5k75k75j, &5k75k75j, &5k75j82j, &1175k75j, &8f24030j
    .dw &0j30q25j, &5k75k75j, &5k75k75j, &5k75k75j, &5k75k75j, &5k75k75j
    .dw &5k75k75j, &5k75q288, &4030j30j, &0q25k75j, &5k75k75j, &5k75k75j
    .dw &5k75k75j, &5k75k75j, &5k75k75j, &5k75k75j, &5q28900j, &0j30j388
    .dw &5k75k75j, &5k75k75j, &5k75k75j, &5k75k75j, &5k75k75j, &5k75k75j
    .dw &5k75k788, &8900j30j, &0q25k75j, &5k75k75j, &5k75k75j, &5k75k75j
    .dw &5k75k75j, &5k75k75j, &5k75k75j, &5k75q288, &4030j388, &5k75k70j
    .dw &0q28f288, &8975k75j, &5k75k75j, &5k75k75j, &5k78830j, &8f28f288
    .dw &5k75q288, &4030q25j, &5k78f20j, &0j38f288, &8f28975j, &5k75k75j
    .dw &5k75k75j, &5q20j30j, &8f28f288, &8975k788, &8830j320, &j651868j
    .dw &346543f8, &3637500j, &1228975j, &5q28f288, &8f28f288, &8f25k75j
    .dw &5k75k75j, &5k75k720, &2848f288, &8f28f288, &8f25k75j, &5q20j30j
    .dw &229w79g8, &44394694, &k6k351k4, &4031225j, &5k75q288, &8f28f288
    .dw &8f28f25j, &5k75k75j, &5k75k75j, &5k78f288, &8f28f288, &8f25k75j
    .dw &5q28900j, &8975k75j, &5q28f288, &8f28f288, &5k75k75j, &5k75k75j
    .dw &5k75k75j, &8f28f288, &8f28975j, &5k75k788, &4228975j, &5k75k75j
    .dw &5j828488, &20f1175j, &5k75k75j, &5k75k75j, &5k75k75j, &5k75k788
    .dw &2161175j, &5k75k75j, &5k789088, &8975k75j, &5k75k75j, &5k75k75j
    .dw &5k75k75j, &5k75k75j, &5k75k75j, &5k75k75j, &5k75k75j, &5k75k788
    .dw &4228975j, &5k75k75j, &5k75k75j, &5k75k75j, &5q25k75j, &5q25k75j
    .dw &5k75k75j, &5k75k75j, &5k75k75j, &5q240388, &5k75k75j, &5k720f10
    .dw &8883j45j, &5k75k75j, &5k75k788, &8f25k75j, &5k75k75j, &5k78f21j
    .dw &5k75k75j, &5q28900j, &8f25k75j, &5j82jg2j, &2jg2j488, &5k75k75j
    .dw &5k75k788, &5k75k75j, &5k75k720, &2jg2jg2j, &2j48975j, &5k78900j
    .dw &0q25k75j, &8882jg2j, &2jg2jg10, &5k75k75j, &5k75k788, &5k75k75j
    .dw &5k75j858, &2jg2jg2j, &2jg1175j, &5q28900j, &0j38975j, &5j82jg2j
    .dw &2jg2jg10, &5k75k75j, &5k75k788, &5k75k75j, &5k75j82j, &2jg2jg2j
    .dw &2j48975j, &8f24030j, &0j38975j, &5q220g2j, &78g1175j, &5k75k75j
    .dw &5k75q25j, &5k75k75j, &5k75k788, &20g2j488, &5k75q288, &4030j30j
    .dw &0q221q10, &5k75k75j, &5k75k75j, &5k75k75j, &8f22k75j, &5k75k75j
    .dw &5k75k75j, &5k75q288, &4030j30j, &0j38f25j, &5k75k75j, &5k75k75j
    .dw &5q220w10, &5k75q25j, &5k75k75j, &5k75k75j, &5q28900j, &0j30j30j
    .dw &0j38f25j, &5k75k75j, &5k75k75j, &5k75k75j, &5k75k75j, &5k75k75j
    .dw &8f24030j, &0j30j30j, &0j30jg88, &8975k75j, &5k75k75j, &5k75k75j
    .dw &5k75k75j, &5q28f240, &0j30j30j, &0j30j30j, &0j30j388, &8f220g10
    .dw &5k75k75j, &5k75k75j, &5q28f288, &4030j30j, &0j30j30j, &0j30j30j
    .dw &0j30j30j, &0q28f288, &8f221640, &40410412
