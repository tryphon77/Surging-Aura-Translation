FUN_354a
	moveq	#6, d7
	lea	(0xff3b54), a0
@process_text
	tst.b	(0xe, a0)
	beq	@next_text
	movea.l	(0x16, a0), a6
	cmpi.b	#2, (0xd, a0)
	bcs	@next_glyph
	subq.b	#1, (0xd, a0)
	bra	@next_text
@next_glyph
	move.b	(0xc,a0), (0xd, a0)
	movea.l	(0x12, a0), a1
	move.b	(a1)+, d0
	andi.l	#0xff, d0
;	cmpi.b	#0xf0, d0
;	bcc	@two_bytes_code

	cmpi.b	#0x20, d0
	bcc	@no_control_code

	addq.l	#1, (0x12, a0)
	lea	(ptrToControlCodesFuns), a2
	andi.l	#0xff, d0
	lsl.w	#2, d0
	movea.l	(a2, d0), a3
	jsr	(a3)
	clr.b	(0xd, a0)
	lsr.b	#2, d0
	cmpi.b	#9, d0
	beq	@next_text

	bra	@process_text
;@two_bytes_code
;	movea.l	(0xff3b36), a4
;	movea.l	(0xff3b42), a5
;	lsl.w	#8, d0
;	add.b	(a1)+, d0
;	andi.l	#0xfff, d0
;	lsl.l	#5, d0
;	moveq	#2, d4
;	move.b	(8, a0), d1
;	subi.b	#2, d1
;	cmp.b	(0xa, a0), d1
;	bcc	@no_cr

;	jsr	controlCode0d 

;@no_cr
;	bra	@draw_char

@no_control_code

;	tst.b	(a0)
;	beq	@cat_03_code

;	movea.l	(0xff3b32), a4
;	movea.l	(0xff3b3e), a5
;	moveq	#0, d4
;	bra	@check_lowercase

;@cat_03_code
;	tst.b	(0xf, a0)
;	beq	@cat_01_code

;	movea.l	(0xff3b46), a4
;	movea.l	(0xff3b4a), a5
;	lea	(0xb6308), a4
;	lea	(0xb850c), a5
	lea	(0xb4100), a4
	lea	(0xb5204), a5
;	moveq	#3, d4
;	bra	@check_lowercase

;@cat_01_code
;	movea.l	(0xff3b2e), a4
;	movea.l	(0xff3b3a), a5
	moveq	#1, d4
;@check_lowercase
;	cmpi.b	#0x40, d0
;	bcs	@skip1

;	cmpi.b	#0x60, d0
;	bcs	@latin
;	bra	@check_katakana

;@latin
;	tst.b	(5, a0)
;	beq	@skip1
;	addi.w	#0x20, d0
;	bra	@skip1

;@check_katakana
;	addi.w	#0x20, d0
;	tst.b	(4, a0)
;	beq	@skip1
;	addi.w	#0x58, d0
;@skip1
	jsr	0x39da
	subi.w	#0x20, d0
;	tst.b	(0xf, a0)
;	beq	@narrow

;	lsl.l	#5, d0
;	bra	@draw_char

;@narrow
;	move.b	(a0), d1
;	andi.l	#0xff, d1
	lsl.l	#4, d0
;	lsr.l	d1, d0
@draw_char
	move.b	(0xa, a0), d1
	move.b	(0xb, a0), d2
	adda.l	d0, a4
	adda.l	d0, a5
	andi.l	#0xff, d1
	andi.l	#0xff, d2
	move.b	(a0), d3
	moveq	#1, d5
	sub.b	d3, d5
	lsl.l	d5, d1
	lsl.l	d5, d2
	moveq	#0, d5
	move.b	(8, a0), d5
	mulu.w	d2, d5
	add.l	d1, d5
	move.w	d5, d0
	add.w	(0x10, a0), d0
	move.b	(1, a0), d1
	move.b	(2, a0), d2
	move.b	(3, a0), d3
	exg	a4, a0
	movea.l	a4, a1
	movea.l	a5, a2
	jsr	0x39fc
	exg	a4, a0
	move.b	(0xa, a0), d1
	move.b	(0x8, a0), d2
	move.b	(0xb, a0), d3
	addq.l	#1, d1
	cmpi.b	#2, d4
	bcs	@skip2
	addq.l	#1, d1
@skip2
	move.b	d1, (0xa, a0)
	move.b	d3, (0xb, a0)
	movea.l	(0x12, a0), a1
	addq.l	#1, a1
	cmpi.b	#2, d4
	bne	@skip3
	addq.l	#1, a1
@skip3
	move.l	a1, (0x12, a0)
	tst.b	(0xd, a0)
	beq	@process_text
@next_text
	adda.l	#0x24, a0
	dbf	d7, @process_text
	rts

