hackStart equ 2171040
ptrToControlCodesFuns	equ	0x373a
controlCode0d	equ	0x39a0


	org	0x377a
	dc.l	controlCode10
	
	org	0x354a
	jmp	FUN_354a
	
	org	hackStart
	include	"asm/dialogs.asm"
	include	"asm/vwf.asm"
