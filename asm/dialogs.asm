controlCode10
	moveq	#0, d0
	move.b	(a1)+, d0
	lsl.w	#8, d0
	move.b	(a1)+, d0
	swap	d0
	move.b	(a1)+, d0
	lsl.w	#8, d0
	move.b	(a1)+, d0

	movea.l	d0, a1
	move.l	d0, 0x12(a0)
	rts
	