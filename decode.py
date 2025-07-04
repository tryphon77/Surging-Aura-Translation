# -*- coding: utf-8 -*-


from buffer import Buffer
from dataclasses import dataclass

@dataclass
class Context:
	pass

def set_flag_buffer(pos):
	print("flag_buffer is at 0x%x" % pos)

def clr_flag(flag_id):
	print("clear flag %d" % flag_id)

def set_flag(flag_id):
	print("set flag %d" % flag_id)


max_iters = 50
param = 0

def fun_7a62(src, ram):
	# In: 
	#	a5: dest (vram)
	#	a6: src
	# Uses:
	#	a0, d0, param
	
	global param
	
	# FUN_00007a62
	# movea.l    A5,A4
	# moveq      #0x0 ,D0
	# LAB_00007a66
	# move.b     (A6)+,D0b
	# beq.b      LAB_00007a66
	# lsl.w      #0x2 ,D0w
	# movea.l    (PTR_fun7a72_00_00007a72 ,PC,D0w *0x1 ),A0
	# jmp        (A0)

	while True:	
		while True:
			cmd = src.read_b()
			if cmd:
				break
		
		print("7a62: cmd=%02x" % cmd)
		if cmd in [0, 0x12, 0x13, 0x24]:
			# fun7a72_00
			# bra.w      FUN_00007a62
			continue
		
		elif cmd in [0x10, 0x14, 0x15, 0x16, 0x17]:
			# fun7a72_10
			# movea.l    (A6),A6
			# bra.w      FUN_00007a62

			# jump
			pos = src.read_l()
			src.set_pos(pos)
			
		elif cmd == 0x18:
			# fun7a72_18
			# bsr.w      FUN_000081e0
			# movea.l    D0,A6
			# bra.w      FUN_00007a62
			src.set_pos(fun_81e0(src))			
			
		elif cmd == 0x11:
			# fun7a72_11
			# movea.l    (A6)+,A0
			# move.l     A0,-(SP)
			# bsr.w      FUN_000081e0
			# movea.l    (SP)+,A0
			# tst.l      D0
			# bne.w      FUN_00007a62
			# movea.l    A0,A6
			# bra.w      FUN_00007a62
			pos = src.read_l()
			if fun_81e0(src) == 0:
				src.set_pos(pos)


		elif cmd == 0x20:
			# fun7a72_20
			# bsr.w      getBitInFf00e6
			# bclr.b     D1,(0x0 ,A0,D2w *0x1)
			# movem.l    {  A0 D2 D1},-(SP)
			# bsr.w      FUN_000081e0
			# movem.l    (SP)+, {  D1 D2 A0}
			# tst.l      D0
			# beq.w      FUN_00007a62
			# bset.b     D1,(0x0 ,A0,D2w *0x1 )
			# bra.w      FUN_00007a62
			bit_id = src.read_b()
			ram.clear_bit(bit_id % 8, 0xe6 + bit_id//8)
			val = fun_81e0(src)
			if val:
				ram.set_bit(bit_id % 8, 0xe6 + bit_id//8)
			
		elif cmd == 0x21:
			# fun7a72_21
			# move.w     (A6)+,D1w
			# move.w     D1w ,-(SP)
			# bsr.w      FUN_000081e0
			# move.w     (SP)+,D1w
			# lea        (DAT_00ff01e6 ).l,A0
			# move.b     D0b ,(0x0 ,A0,D1w *0x1)
			# bra.w      FUN_00007a62
			offset = src.read_w()
			val = fun_81e0(src)
			ram.write_b(val, 0x1e6 + offset)
			
		elif cmd == 0x22:
			# fun7a72_22
			# move.w     (A6)+,D1w
			# move.w     D1w ,-(SP)
			# bsr.w      FUN_000081e0
			# move.w     (SP)+,D1w
			# lea        (DAT_00ff03e6 ).l,A0
			# add.w      D1w ,D1w
			# move.w     D0w ,(0x0 ,A0,D1w *0x1 )
			# bra.w      FUN_00007a62
			offset = src.read_w()
			val = fun_81e0(src)
			ram.write_w(val, 0x3e6 + 2*offset)
			
		elif cmd == 0x23:
			# fun7a72_23
			# move.b     (A6)+,D1b
			# and.w      #0xff ,D1w
			# move.w     D1w ,-(SP)
			# bsr.w      FUN_000081e0
			# move.w     (SP)+,D1w
			# lea        (DAT_00ff07e6 ).l,A0
			# lsl.w      #0x2 ,D1w
			# move.l     D0,(0x0 ,A0,D1w *0x1 )
			# bra.w      FUN_00007a62
			offset = src.read_b()
			val = fun_81e0(src)
			ram.write_b(val, 0x7e6 + 4*offset)
			
		elif cmd == 0x25:
			# fun7a72_25
			# move.b     (A6)+,D1b
			# and.w      #0xff ,D1w
			# move.w     D1w ,-(SP)
			# bsr.w      FUN_000081e0
			# move.w     (SP)+,D1w
			# move.b     D0b ,(0x4 ,A4,D1w *0x1 )
			# bra.w      FUN_00007a62
			offset = src.read_b()
			val = fun_81e0(src)
			ram.write_b(val, ram.pos + 4 + offset)

	
		elif cmd == 0x50:
			# fun7a72_50
			# bsr.w      FUN_000081e0
			# move.b     D0b ,(0x4 ,A4)
			# bra.w      FUN_00007a62
			val = fun_81e0(src)
			ram.write_b(val, ram.pos + 4)
			
		elif cmd == 0x51:
			# fun7a72_51
			# bsr.w      FUN_000081e0
			# move.b     D0b ,(0x5 ,A4)
			# bra.w      FUN_00007a62
			val = fun_81e0(src)
			ram.write_b(val, ram.pos + 5)
			
		elif cmd == 0x52:
			# fun7a72_52
			# bsr.w      FUN_000081e0
			# move.b     D0b ,(0x6 ,A4)
			# bra.w      FUN_00007a62
			val = fun_81e0(src)
			ram.write_b(val, ram.pos + 6)
			
		elif cmd == 0x53:
			# fun7a72_53
			# bsr.w      FUN_000081e0
			# move.b     D0b ,(0x7 ,A4)
			# bra.w      FUN_00007a62
			val = fun_81e0(src)
			ram.write_b(val, ram.pos + 7)
			
		elif cmd == 0x26:
			# fun7a72_26
			# move.b     (A6)+,D1b
			# and.w      #0xff ,D1w
			# move.w     D1w ,-(SP)
			# bsr.w      FUN_000081e0
			# move.w     (SP)+,D1w
			# add.w      D1w ,D1w
			# move.w     D0w ,(0x8 ,A4,D1w *0x1 )
			# bra.w      FUN_00007a62
			offset = src.read_b()
			val = fun_81e0(src)
			ram.write_w(val, ram.pos + 8 + 2*offset)
			
		elif cmd == 0x54:
			# fun7a72_54
			# bsr.w      FUN_000081e0
			# move.w     D0w ,(0x8 ,A4)
			# bra.w      FUN_00007a62
			val = fun_81e0(src)
			ram.write_w(val, ram.pos + 8)
			
		elif cmd == 0x55:
			# fun7a72_55
			# bsr.w      FUN_000081e0
			# move.w     D0w ,(0xa ,A4)
			# bra.w      FUN_00007a62
			val = fun_81e0(src)
			ram.write_w(val, ram.pos + 10)
			
		elif cmd == 0x56:
			# fun7a72_56
			# bsr.w      FUN_000081e0
			# move.w     D0w ,(0xc ,A4)
			# bra.w      FUN_00007a62
			val = fun_81e0(src)
			ram.write_w(val, ram.pos + 12)
			
		elif cmd == 0x57:
			# fun7a72_57
			# bsr.w      FUN_000081e0
			# move.w     D0w ,(0xe ,A4)
			# bra.w      FUN_00007a62
			val = fun_81e0(src)
			ram.write_w(val, ram.pos + 14)
			
		elif cmd == 0x27:
			# fun7a72_27
			# move.b     (A6)+,D1b
			# and.w      #0xff ,D1w
			# move.w     D1w ,-(SP)
			# bsr.w      FUN_000081e0
			# move.w     (SP)+,D1w
			# lsl.w      #0x2 ,D1w
			# move.l     D0,(0x10 ,A4,D1w *0x1 )
			# bra.w      FUN_00007a62
			offset = src.read_b()
			val = fun_81e0(src)
			ram.write_l(val, ram.pos + 16 + 4*offset)
			
		elif cmd == 0x58:
			# fun7a72_58
			# bsr.w      FUN_000081e0
			# move.l     D0,(0x10 ,A4)
			# bra.w      FUN_00007a62
			val = fun_81e0(src)
			ram.write_l(val, ram.pos + 16)
			
		elif cmd == 0x59:
			# fun7a72_59
			# bsr.w      FUN_000081e0
			# move.l     D0,(0x14 ,A4)
			# bra.w      FUN_00007a62
			val = fun_81e0(src)
			ram.write_l(val, ram.pos + 20)
			
		elif cmd == 0x5a:
			# fun7a72_5a
			# bsr.w      FUN_000081e0
			# move.l     D0,(0x18 ,A4)
			# bra.w      FUN_00007a62
			val = fun_81e0(src)
			ram.write_l(val, ram.pos + 24)
			
		elif cmd == 0x5b:
			# fun7a72_5b
			# bsr.w      FUN_000081e0
			# move.l     D0,(0x1c ,A4)
			# bra.w      FUN_00007a62
			val = fun_81e0(src)
			ram.write_l(val, ram.pos + 28)
			
		elif cmd == 0x5c:
			# fun7a72_5c
			# bsr.w      FUN_000081e0
			# move.l     D0,(0x20 ,A4)
			# bra.w      FUN_00007a62
			val = fun_81e0(src)
			ram.write_l(val, ram.pos + 32)
			
		elif cmd == 0x5d:
			# fun7a72_5d
			# bsr.w      FUN_000081e0
			# move.l     D0,(0x24 ,A4)
			# bra.w      FUN_00007a62
			val = fun_81e0(src)
			ram.write_l(val, ram.pos + 36)
			
		elif cmd == 0x5e:
			# fun7a72_5e
			# bsr.w      FUN_000081e0
			# move.l     D0,(0x28 ,A4)
			# bra.w      FUN_00007a62
			val = fun_81e0(src)
			ram.write_l(val, ram.pos + 40)
			
		elif cmd == 0x5f:
			# fun7a72_5f
			# bsr.w      FUN_000081e0
			# move.l     D0,(0x2c ,A4)
			# bra.w      FUN_00007a62
			val = fun_81e0(src)
			ram.write_l(val, ram.pos + 44)
	

		elif cmd == 0x28:
			# fun7a72_28
			# move.b     (A6)+,D1b
			# and.w      #0xff ,D1w
			# move.w     D1w ,-(SP)
			# bsr.w      FUN_000081e0
			# move.w     (SP)+,D1w
			# lsl.w      #0x2 ,D1w
			# lea        (DAT_00ff00a6).l,A0
			# move.l     D0,(0x0 ,A0,D1w *0x1 )
			# bra.w      FUN_00007a62
			offset = src.read_b()
			val = fun_81e0()
			ram.write_l(val, 0xa6 + 4*offset)
			
		elif cmd == 0x29:
			# fun7a72_29
			# move.b     (A6)+,D1b
			# and.w      #0xff ,D1w
			# move.w     D1w ,-(SP)
			# bsr.w      FUN_000081e0
			# move.w     (SP)+,D1w
			# lsl.w      #0x2 ,D1w
			# lea        (DAT_00ff00b6 ).l,A0
			# move.l     D0,(0x0 ,A0,D1w *0x1 )
			# bra.w      FUN_00007a62
			offset = src.read_b()
			val = fun_81e0()
			ram.write_l(val, 0xb6 + 4*offset)
			
		elif cmd == 0x2a:
			# fun7a72_2a
			# move.b     (A6)+,D1b
			# and.w      #0xff ,D1w
			# move.w     D1w ,-(SP)
			# bsr.w      FUN_000081e0
			# move.w     (SP)+,D1w
			# lsl.w      #0x2 ,D1w
			# lea        (DAT_00ff00c6 ).l,A0
			# move.l     D0,(0x0 ,A0,D1w *0x1 )
			# bra.w      FUN_00007a62
			offset = src.read_b()
			val = fun_81e0()
			ram.write_l(val, 0xc6 + 4*offset)
			
		elif cmd == 0x2b:
			# fun7a72_2b
			# move.b     (A6)+,D1b
			# and.w      #0xff ,D1w
			# move.w     D1w ,-(SP)
			# bsr.w      FUN_000081e0
			# move.w     (SP)+,D1w
			# lsl.w      #0x2 ,D1w
			# lea        (DAT_00ff00d6 ).l,A0
			# move.l     D0,(0x0 ,A0,D1w *0x1 )
			# bra.w      FUN_00007a62
			offset = src.read_b()
			val = fun_81e0()
			ram.write_l(val, 0xd6 + 4*offset)
			
		elif cmd == 0x2c:
			# fun7a72_2c
			# move.b     (A6)+,D1b
			# and.w      #0xff ,D1w
			# lsl.w      #0x2 ,D1w
			# lea        (DAT_00ff00a6 ).l,A0
			# movea.l    (0x0 ,A0,D1w *0x1 ),A0
			# move.l     A0,-(SP)
			# bsr.w      FUN_000081e0
			# movea.l    (SP)+,A0
			# move.w     D0w ,D1w
			# move.w     D0w ,D2w
			# lsr.w      #0x3 ,D1w
			# bclr.b     D2,(0x0 ,A0,D1w *0x1 )
			# movem.l    {  A0 D2 D1},-( SP)
			# bsr.w      FUN_000081e0
			# movem.l    (SP)+, {  D1 D2 A0}
			# tst.l      D0
			# beq.w      FUN_00007a62
			# bset.b     D2,(0x0 ,A0,D1w *0x1 )
			# bra.w      FUN_00007a62
			offset = src.read_b()
			pos = ram.read_l(0xa6 + 4*offset)

			val1 = fun_81e0()
			ram.clear_bit(val1 % 8, pos + val1//8)
			
			val2 = fun_81e0()
			if val2 != 0:
				ram.set_bit(val1 % 8, pos + val1//8)
			
		elif cmd == 0x2d:
			# fun7a72_2d
			# move.b     (A6)+,D1b
			# and.w      #0xff ,D1w
			# move.w     D1w ,-(SP)
			# bsr.w      FUN_000081e0
			# move.w     (SP)+,D1w
			# lsl.w      #0x2 ,D1w
			# lea        (DAT_00ff00b6 ).l,A0
			# movea.l    (0x0 ,A0,D1w *0x1 ),A0
			# move.w     D0w ,D1w
			# movem.l    {  A0 D1},-( SP)
			# bsr.w      FUN_000081e0
			# movem.l    (SP)+, {  D1 A0}
			# move.b     D0b ,(0x0 ,A0,D1w *0x1 )
			# bra.w      FUN_00007a62
			offset = src.read_b()
			pos = ram.read_l(0xb6 + 4*offset)

			val1 = fun_81e0()
			ram.clear_bit(val1 % 8, pos + val1//8)
			
			val2 = fun_81e0()
			if val2 != 0:
				ram.set_bit(val1 % 8, pos + val1//8)
			
		elif cmd == 0x2e:
			# fun7a72_2e
			# move.b     (A6)+,D1b
			# and.w      #0xff ,D1w
			# move.w     D1w ,-(SP)
			# bsr.w      FUN_000081e0
			# move.w     (SP)+,D1w
			# lsl.w      #0x2 ,D1w
			# lea        (DAT_00ff00c6 ).l,A0
			# movea.l    (0x0 ,A0,D1w *0x1 ),A0
			# add.w      D0w ,D0w
			# move.w     D0w ,D1w
			# movem.l    {  A0 D1},-( SP)
			# bsr.w      FUN_000081e0
			# movem.l    (SP)+, {  D1 A0}
			# move.w     D0w ,(0x0 ,A0,D1w *0x1 )
			# bra.w      FUN_00007a62
			offset = src.read_b()
			pos = ram.read_l(0xc6 + 4*offset)

			val1 = fun_81e0()
			ram.clear_bit(val1 % 8, pos + val1//8)
			
			val2 = fun_81e0()
			if val2 != 0:
				ram.set_bit(val1 % 8, pos + val1//8)
			
		elif cmd == 0x2f:
			# fun7a72_2f
			# move.b     (A6)+,D1b
			# and.w      #0xff ,D1w
			# move.w     D1w ,-(SP)
			# bsr.w      FUN_000081e0
			# move.w     (SP)+,D1w
			# lsl.w      #0x2 ,D1w
			# lea        (DAT_00ff00d6 ).l,A0
			# movea.l    (0x0 ,A0,D1w *0x1 ),A0
			# lsl.w      #0x2 ,D0w
			# move.w     D0w ,D1w
			# movem.l    {  A0 D1},-( SP)
			# bsr.b      FUN_000081e0
			# movem.l    (SP)+, {  D1 A0}
			# move.l     D0,(0x0 ,A0,D1w *0x1 )
			# bra.w      FUN_00007a62
			offset = src.read_b()
			pos = ram.read_l(0xc6 + 4*offset)

			val1 = fun_81e0()
			ram.clear_bit(val1 % 8, pos + val1//8)
			
			val2 = fun_81e0()
			if val2 != 0:
				ram.set_bit(val1 % 8, pos + val1//8)
		
		elif cmd == 0x40:
			# fun7a72_40
			# movem.l    {  A4 D7},-( SP)
			# lea        (-0x20 ,A5),A5
			# move.l     (A6)+,-(SP)
			# bsr.b      FUN_000081cc
			# lea        (-0xc ,A5),A5
			# move.l     A6,-(A5)
			# movea.l    (SP)+,A6
			# bsr.w      FUN_00007a62
			# movea.l    (A5)+,A6
			# lea        (0x28 ,A5),A5
			# move.l     (A5)+,D0
			# movem.l    (SP)+, {  D7 A4}
			# bra.w      FUN_00007a62
			ram.advance_by(-32)
			new_pos = src.read_l()
			fun_81cc(src, ram)
			ram.advance_by(-16)
			ram.write_l(src.pos, ram.pos)
			ram.advance_by(-4)			
			src.set_pos(new_pos)
			fun_7a62(src, ram)
			src.set_pos(ram.read_l())
			ram.advance_by(40)
			src.read_l()	
	
		elif cmd == 0x41:			
			# fun7a72_41
			# move.l     D7,-(SP)
			# lea        (-0x20 ,A5),A5
			# move.l     (A6)+,-(SP)
			# bsr.b      FUN_000081cc
			# movea.l    (SP)+,A0
			# movem.l    {  A6 A5 A4},-( SP)
			# jsr        (A0)
			# movem.l    (SP)+, {  A4 A5 A6}
			# lea        (0x20 ,A5),A5
			# move.l     (SP)+,D7
			# bra.w      FUN_00007a62
			
			# save d7
			ram.advance_by(-32)
	
			routine_pos = src.read_l()
			fun_81cc()
			
			src.push()
			ram.push()
			print("jsr 0x%x" % routine_pos)
			ram.pop()
			src.pop()
			
			ram.advance_by(32)
			# restore d7

		elif cmd in [0x3f, 0xff]:
			break

		else:
			raise Exception("Unknown cmd: %s" % cmd)				
	
			
			
def fun_81cc(src, ram):
	print("81cc")
	# FUN_000081cc ()
	# movea.l    A5,A3
	# LAB_000081ce
	# move.l     A3,-(SP)
	# bsr.b      FUN_000081e0
	# movea.l    (SP)+,A3
	# move.l     D0,(A3)+
	# cmpi.b     #0xFFF0 ,(-0x1 ,A6)
	# beq.b      LAB_000081ce
	# rts
	
	ram.push()
	
	while True:
		ram.push()
		data = fun_81e0(src, ram)
		print("81cc: data=%02x" % data)
		ram.pop()
		ram.write_l(data)
		if src.read_b(src.pos - 1) == 0xf0:
			break	
	ram.pop()

def fun_81e0(src, ram):
	print("81e0")
	global param
	# FUN_000081e0
	# movem.l    {  D7 D6},-( SP)
	# moveq      #0x0 ,D7
	# cmpi.b     #0xFFF0 ,(A6)
	# bcc.b      LAB_000081fa
	# bsr.b      FUN_00008204
	# move.l     D0,D7
	# LAB_000081f0
	# bsr.w      FUN_0000885a
	# cmpi.b     #-0x10 ,(A6)
	# bcs.b      LAB_000081f0
	# LAB_000081fa
	# move.l     D7,D0
	# addq.l     #0x1 ,A6
	# movem.l    (SP)+, {  D6 D7}
	# rts
	
	param_temp = param # save d7/d6
	param = 0
	if src.read_b(pos=src.pos) < 0xf0:
		param = fun_8204(src, ram)
	
		# save d7
		while src.read_b(pos=src.pos) < 0xf0:
			print("before: param=%x" % param)
			param = fun_885a(src, ram, param)
			print("after: param=%x" % param)
	
	src.read_b()
	param = param_temp # restore d7/d6
	return param

def fun_8204(src, ram):
	# FUN_00008204
	# moveq      #0x0 ,D0
	# LAB_00008206
	# move.b     (A6)+,D0b
	# beq.b      LAB_00008206
	# lsl.w      #0x2 ,D0w
	# movea.l    (PTR_fun8212_00_00008212 ,PC,D0w *0x1 ),A0
	# jmp        (A0)

	while True:
		val = src.read_b()
		if val != 0:
			break

	print("8204: val=%02x" % val)

	if val == 00:
		return 0
		
	elif val in [0xf0, 0xf1]:
		src.advance_by(-1)
		return 0
	
	elif val == 0xa0:
		return src.read_b()
	
	elif val == 0xa1:
		return src.read_w()

	elif val == 0xa2:
		return src.read_l()

	elif val == 0x20:
		# fun8212_20_checkBitInFf00e6
		# bsr.w      getBitInFf00e6
		# moveq      #0x0 ,D0
		# btst.b     D1,(0x0 ,A0,D2w *0x1 )
		# beq.b      LAB_00008636
		# subq.l     #0x1 ,D0
		# LAB_00008636
		# rts
		
		bit_id = src.read_b()
		return ram.test_bit(bit_id % 8, 0xe6 + bit_id//8)
	
	elif val == 0x21:
		# fun8212_21
		# move.w     (A6)+,D1w
		# lea        (DAT_00ff01e6 ).l,A0
		# moveq      #0x0 ,D0
		# move.b     (0x0 ,A0,D1w *0x1), D0
		# rts
		
		return ram.read_b(0x1e6 + src.read_w())

	elif val == 0x22:
		# fun8212_22
		# move.w     (A6)+,D1w
		# lea        (DAT_00ff03e6 ).l,A0
		# add.w      D1w ,D1w
		# moveq      #0x0 ,D0
		# move.w     (0x0 ,A0,D1w *0x1), D0w
		# rts

		return ram.read_w(0x3e6 + src.read_w())
	
	elif val == 0x23:
		# fun8212_23
		# moveq      #0x0 ,D1
		# move.b     (A6)+,D1b
		# lsl.w      #0x2 ,D1w
		# lea        (DAT_00ff07e6 ).l,A0
		# move.l     (0x0 ,A0,D1w*0x1),D0
		# rts

		return ram.read_w(0x7e6 + src.read_l())

	elif val == 0x24:
		# fun8212_24
		# move.b     (A6)+,D1b
		# moveq      #0x0 ,D0
		# btst.b     D1,(0x4 ,A4)
		# beq.b      LAB_00008678
		# subq.l     #0x1 ,D0
		# LAB_00008678
		# rts
		
		bit_id = src.read_b()
		return ram.test_bit(bit_id, ram.pos + 4)
		
	elif val == 0x25:		
		# fun8212_25
		# moveq      #0x0 ,D1
		# move.b     (A6)+,D1b
		# moveq      #0x0 ,D0
		# move.b     (0x4 ,A4,D1w *0x1 ),D0b
		# rts
		offset = src.read_b()
		return ram.read_b(ram.pos + offset)

	elif val == 0x50:
		# fun8212_50
		# moveq      #0x0 ,D0
		# move.b     (0x4 ,A4),D0b
		# rts
		return ram.read_b(ram.pos + 4)
	
	elif val == 0x51:
		# fun8212_51
		# moveq      #0x0 ,D0
		# move.b     (0x5 ,A4),D0b
		# rts
		return ram.read_b(ram.pos + 5)
		
	elif val == 0x52:
		# fun8212_52
		# moveq      #0x0 ,D0
		# move.b     (0x6 ,A4),D0b
		# rts
		return ram.read_b(ram.pos + 6)
		
	elif val == 0x53:
		# fun8212_53
		# moveq      #0x0 ,D0
		# move.b     (0x7 ,A4),D0b
		# rts
		return ram.read_b(ram.pos + 7)

	
	elif val == 0x26:
		# fun8212_26
		# moveq      #0x0 ,D1
		# move.b     (A6)+,D1b
		# add.w      D1w ,D1w
		# moveq      #0x0 ,D0
		# move.w     (0x8 ,A4,D1w *0x1 ),D0w
		# rts
		offset = src.read_b()
		return ram.read_w(ram.pos + 2*offset)
		
	elif val == 0x54:
		# fun8212_54
		# moveq      #0x0 ,D0
		# move.w     (0x8 ,A4),D0w
		# rts
		return ram.read_w(ram.pos + 8)
		
	elif val == 0x55:
		# fun8212_55
		# moveq      #0x0 ,D0
		# move.w     (0xa ,A4),D0w
		# rts
		return ram.read_w(ram.pos + 10)
		
	elif val == 0x56:
		# fun8212_56
		# moveq      #0x0 ,D0
		# move.w     (0xc ,A4),D0w
		# rts
		return ram.read_w(ram.pos + 12)
		
	elif val == 0x57:
		# fun8212_57
		# moveq      #0x0 ,D0
		# move.w     (0xe ,A4),D0w
		# rts
		return ram.read_w(ram.pos + 14)

	elif val == 0x27:
		# fun8212_27
		# moveq      #0x0 ,D1
		# move.b     (A6)+,D1b
		# lsl.w      #0x2 ,D1w
		# move.l     (0x10 ,A4,D1w *0x1 ),D0
		# rts
		offset = src.read_b()
		return ram.read_l(ram.pos + 16 + 4*offset)
		
	elif val == 0x58:
		# fun8212_58
		# move.l     (0x10 ,A4),D0
		# rts
		return ram.read_l(ram.pos + 16)
		
	elif val == 0x59:
		# fun8212_59
		# move.l     (0x14 ,A4),D0
		# rts
		return ram.read_l(ram.pos + 20)
		
	elif val == 0x5a:
		# fun8212_5a
		# move.l     (0x18 ,A4),D0
		# rts
		return ram.read_l(ram.pos + 24)
		
	elif val == 0x5b:
		# fun8212_5b
		# move.l     (0x1c ,A4),D0
		# rts
		return ram.read_l(ram.pos + 28)
		
	elif val == 0x5c:
		# fun8212_5c
		# move.l     (0x20 ,A4),D0
		# rts
		return ram.read_l(ram.pos + 32)
		
	elif val == 0x5d:
		# fun8212_5d
		# move.l     (0x24 ,A4),D0
		# rts
		return ram.read_l(ram.pos + 36)
		
	elif val == 0x5e:
		# fun8212_5e
		# move.l     (0x28 ,A4),D0
		# rts
		return ram.read_l(ram.pos + 40)
		
	elif val == 0x5f:
		# fun8212_5f
		# move.l     (0x2c ,A4),D0
		# rts
		return ram.read_l(ram.pos + 44)
		
	elif val == 0x28:
		# fun8212_28
		# move.b     (A6)+,D1b
		# and.w      #0xff ,D1w
		# lsl.w      #0x2 ,D1w
		# lea        (DAT_00ff00a6 ).l,A0
		# move.l     (0x0 ,A0,D1w),D0
		# rts
		offset = src.read_b()
		return ram.read_l(0xa6 + 4*offset)
		
	elif val == 0x29:
		# fun8212_29
		# move.b     (A6)+,D1b
		# and.w      #0xff ,D1w
		# lsl.w      #0x2 ,D1w
		# lea        (DAT_00ff00b6 ).l,A0
		# move.l     (0x0 ,A0,D1w *0x1 )=>DAT_00ff00b6 ,D0
		# rts
		offset = src.read_b()
		return ram.read_l(0xb6 + 4*offset)
		
	elif val == 0x2a:
		# fun8212_2a
		# move.b     (A6)+,D1b
		# and.w      #0xff ,D1w
		# lsl.w      #0x2 ,D1w
		# lea        (DAT_00ff00c6 ).l,A0
		# move.l     (0x0 ,A0,D1w), D0
		# rts
		offset = src.read_b()
		return ram.read_l(0xc6 + 4*offset)
		
	elif val == 0x2b:
		# fun8212_2b
		# move.b     (A6)+,D1b
		# and.w      #0xff ,D1w
		# lsl.w      #0x2 ,D1w
		# lea        (DAT_00ff00d6 ).l,A0
		# move.l     (0x0 ,A0,D1w), D0
		# rts
		offset = src.read_b()
		return ram.read_l(0xd6 + 4*offset)
		
	elif val == 0x2c:
		# fun8212_2c
		# moveq      #0x0 ,D1
		# move.b     (A6)+,D1b
		# lsl.w      #0x2 ,D1w
		# lea        (DAT_00ff00a6 ).l,A0
		# movea.l    (0x0 ,A0,D1w *0x1 )=>DAT_00ff00a6 ,A0
		# move.l     A0,-(SP)=>local_4
		# bsr.w      FUN_000081e0
		# movea.l    (SP)+,A0
		# move.w     D0w ,D1w
		# move.w     D0w ,D2w
		# lsr.w      #0x3 ,D1w
		# moveq      #0x0 ,D0
		# btst.b     D2,(0x0 ,A0,D1w *0x1 )
		# beq.b      LAB_00008788
		# subq.l     #0x1 ,D0
		# LAB_00008788
		# rts
		offset = src.read_b()
		addr = ram.read_l(0xa6 + 4*offset)

		bit_id = fun_81e0(src)
		
		return ram.test_bit(bit_id % 8, addr + bit_id//8)
		
	elif val == 0x2d:
		# fun8212_2d
		# moveq      #0x0 ,D1
		# move.b     (A6)+,D1b
		# move.w     D1w ,-(SP)=>local_4 +0x2
		# bsr.w      FUN_000081e0
		# move.w     (SP)+,D1w
		# lsl.w      #0x2 ,D1w
		# lea        (DAT_00ff00b6 ).l,A0
		# movea.l    (0x0 ,A0,D1w),A0
		# move.w     D0w ,D1w
		# moveq      #0x0 ,D0
		# move.b     (0x0 ,A0,D1w *0x1 ),D0b
		# rts
		offset = src.read_b()
		addr = ram.read_l(0xb6 + 4*offset)
				
		return ram.read_b(addr + fun_81e0(src))

				
	elif val == 0x2e:
		# fun8212_2e
		# moveq      #0x0 ,D1
		# move.b     (A6)+,D1b
		# move.w     D1w ,-(SP)=>local_4 +0x2
		# bsr.w      FUN_000081e0
		# move.w     (SP)+,D1w
		# lsl.w      #0x2 ,D1w
		# lea        (DAT_00ff00c6 ).l,A0
		# movea.l    (A0,D1),A0
		# add.w      D0w ,D0w
		# move.w     D0w ,D1w
		# moveq      #0x0 ,D0
		# move.w     (0x0 ,A0,D1w *0x1 ),D0w
		# rts
		offset = src.read_b()
		addr = ram.read_l(0xb6 + 4*offset)
				
		return ram.read_w(addr + 2*fun_81e0(src))
		
	elif val == 0x2f:
		# fun8212_2f
		# moveq      #0x0 ,D1
		# move.b     (A6)+,D1b
		# move.w     D1w ,-(SP)=>local_4 +0x2
		# bsr.w      FUN_000081e0
		# move.w     (SP)+,D1w
		# lsl.w      #0x2 ,D1w
		# lea        (DAT_00ff00d6 ).l,A0
		# movea.l    (A0, D1), A0
		# lsl.w      #0x2 ,D0w
		# move.w     D0w ,D1w
		# move.l     (0x0 ,A0,D1w *0x1 ),D0
		# rts
		offset = src.read_b()
		addr = ram.read_l(0xb6 + 4*offset)
				
		return ram.read_l(addr + 4*fun_81e0(src))

	elif val == 0xaf:
		# fun8212_af
		# move.l     D7,-(SP)
		# bsr.w      FUN_000081e0
		# move.l     (SP)+,D7
		# rts
		return fun_81e0()
		
	elif val == 0xc4:
		# fun8212_c4
		# bsr.w      FUN_00008204
		# not.l      D0
		# rts
		return fun_8204(src, ram) ^ 0xffffffff
		
	elif val == 0xc5:
		# fun8212_c5
		# bsr.w      FUN_00008204
		# neg.l      D0
		# rts
		return -fun_8204(src, ram)
		
	elif val == 0x40:
		# fun8212_40
		# movem.l    { A4 D7},-( SP)
		# lea        (-0x20 ,A5),A5
		# move.l     (A6)+,-(SP)
		# bsr.w      FUN_000081cc
		# lea        (-0xc ,A5),A5
		# move.l     A6,-(A5)
		# movea.l    (SP)+,A6
		# bsr.w      FUN_00007a62
		# movea.l    (A5)+,A6
		# lea        (0x28 ,A5),A5
		# move.l     (A5)+,D0
		# movem.l    (SP)+, {  D7 A4}
		# rts
		ram.set_pos(ram.pos - 0x20)
		new_pos = src.read_l()
		fun_81cc(src)

		ram.set_pos(ram.pos - 0x10)
		ram.write_l(ram.pos)
		
		ram.set_pos(new_pos)
		fun_7a62(src, ram)
		
		src.set_pos(ram.read_l())
		ram.set_pos(ram.pos + 0x24)
		return ram.read_l()
		
	elif val == 0x41:
		# fun8212_41
		# movem.l    {  D7},-( SP)
		# movea.l    (A6)+,A0
		# lea        (-0x20 ,A5),A5
		# move.l     A0,-(SP)
		# bsr.w      FUN_000081cc
		# movea.l    (SP)+,A0
		# movem.l    {  A6 A5 A4},-( SP)
		# jsr        (A0)
		# movem.l    (SP)+, {  A4 A5 A6}
		# lea        (0x20 ,A5),A5
		# movem.l    (SP)+, {  D7}
		# rts
		func_pos = src.read_l()
		ram.set_pos(ram.pos - 0x20)
		fun_81cc(src, ram)
		
		src.push()
		ram.push()
		print("jsr 0x%x" % func_pos)
		ram.pop()
		src.pop()
		
		ram.set_pos(ram.pos + 0x20)
		return -1

	else:
		raise Exception("Unknown cmd: %s" % val)				

def step():
	global max_iters

	max_iters -= 1
	if max_iters == 0:
		raise Exception("Max iterations reacehed")
		
def fun_885a(src, ram, val):	
	step()

	while True:
		cmd = src.read_b()
		if cmd != 0:
			break
	
	print("885a: cmd=%02x" % cmd)

	if cmd == 00:
		# fun885a_00
		# rts
		return val
		
	elif cmd == 0xc8:
		# fun885a_c8
		# bsr.w      FUN_00008204
		# muls.w     D0w ,D7
		# rts
		return val * fun_8204(src, ram)
		
	elif cmd == 0xc9:
		# fun885a_c9
		# bsr.w      FUN_00008204
		# divs.w     D0w ,D7
		# ext.l      D7
		# rts
		return val % fun_8204(src, ram)
		
	elif cmd == 0xca:
		# fun885a_ca
		# bsr.w      FUN_00008204
		# divs.w     D0w ,D7
		# swap       D7
		# ext.l      D7
		# rts
		return val // fun_8204(src, ram)
		
	elif cmd == 0xcc:
		# fun885a_cc
		# bsr.b      FUN_00008d04
		# add.l      D0,D7
		# rts
		return val + fun_8d04(src, ram, cmd)
		
	elif cmd == 0xcd:
		# fun885a_cd
		# bsr.b      FUN_00008d04
		# sub.l      D0,D7
		# rts
		return val - fun_8d04(src, ram, cmd)
		
	elif cmd == 0xd0:
		# fun885a_d0
		# bsr.b      FUN_00008d04
		# cmp.l      D0,D7
		# bcs.b      LAB_00008ca0
		# moveq      #0x0 ,D7
		# rts
		# LAB_00008ca0
		# moveq      #-0x1 ,D7
		# rts
		return val < fun_8d04(src, ram, cmd)
		
	elif cmd == 0xd1:
		# fun885a_d1
		# bsr.b      FUN_00008d04
		# cmp.l      D0,D7
		# bls.b      LAB_00008cae
		# moveq      #0x0 ,D7
		# rts
		# LAB_00008cae
		# moveq      #-0x1 ,D7
		# rts
		return val <= fun_8d04(src, ram, cmd)
		
	elif cmd == 0xd2:
		# fun885a_d2
		# bsr.b      FUN_00008d04
		# cmp.l      D0,D7
		# bhi.b      LAB_00008cbc
		# moveq      #0x0 ,D7
		# rts
		# LAB_00008cbc
		# moveq      #-0x1 ,D7
		# rts
		return val >= fun_8d04(src, ram, cmd)
		
	elif cmd == 0xd3:
		# fun885a_d3
		# bsr.b      FUN_00008d04
		# cmp.l      D0,D7
		# bcc.b      LAB_00008cca
		# moveq      #0x0 ,D7
		# rts
		# LAB_00008cca
		# moveq      #-0x1 ,D7
		# rts
		return val > fun_8d04(src, ram, cmd)
		
	elif cmd == 0xd4:
		# fun885a_d4
		# bsr.b      FUN_00008d04
		# cmp.l      D0,D7
		# beq.b      LAB_00008cd8
		# moveq      #0x0 ,D7
		# rts
		# LAB_00008cd8
		# moveq      #-0x1 ,D7
		# rts
		return val == fun_8d04(src, ram, cmd)
		
	elif cmd == 0xd5:
		# fun885a_d5
		# bsr.b      FUN_00008d04
		# cmp.l      D0,D7
		# bne.b      LAB_00008ce6
		# moveq      #0x0 ,D7
		# rts
		# LAB_00008ce6
		# moveq      #-0x1 ,D7
		# rts
		return val != fun_8d04(src, ram, cmd)
		
	elif cmd == 0xd8:
		# fun885a_d8
		# bsr.b      FUN_00008d04
		# and.l      D0,D7
		# rts
		return val & fun_8d04(src, ram, cmd)
		
	elif cmd == 0xdc:
		# fun885a_dc
		# bsr.b      FUN_00008d04
		# eor.l      D0,D7
		# rts
		return val ^ fun_8d04(src, ram, cmd)
		
	elif cmd == 0xe0:
		# fun885a_e0
		# bsr.b      FUN_00008d04
		# or.l       D0,D7
		# rts
		return val | fun_8d04(src, ram, cmd)
		
	elif cmd in [0xf0, 0xf1]:
		# fun885a_f0
		# subq.l     #0x1 ,A6
		# rts
		
		# fun885a_f1
		# subq.l     #0x1 ,A6
		# rts
		
		src.set_pos(src.pos - 1)
		return val

	else:
		raise Exception("Unknown cmd: %s" % cmd)				

def fun_8d04(src, ram, cmd):
	# FUN_00008d04
	# move.b     D0b ,D6b
	# and.b      #0xFC ,D6b
	# bsr.w      FUN_00008204
	# move.b     (A6),D3b
	# and.b      #0xfc, D3b
	# cmp.b      D6b ,D3b
	# bcc.b      LAB_00008d28
	# movem.l    {  D7 D6},-( SP)
	# move.l     D0,D7
	# bsr.w      FUN_0000885a
	# move.l     D7,D0
	# movem.l    (SP)+, {  D6 D7}
	# LAB_00008d28
	# rts
	first_6_bits = cmd & 0xfc
	val = fun_8204(src, ram)
	if src.read_b(src.pos) <= first_6_bits:
		return fun_885a(src, ram, cmd)
	else:
		print("8d04: val=%02x" % val)
		return val

source = Buffer.load("bin/Surging Aura (Japan).md")
ram = Buffer()

source.set_pos(0x12b16)
ram.set_pos(0x10b6)
fun_7a62(source, ram)


