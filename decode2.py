# -*- coding: utf-8 -*-

from buffer import Buffer
from dataclasses import dataclass
import numpy as np

def warns(text):
	print(text)

source = Buffer.load("bin/Surging Aura (Japan).md")

@dataclass
class Context:
	decoded = np.zeros(0x200000, dtype=np.uint8)
	functions = set()
	candidates = set()
	dialogs = []
	data = set()

context = Context()

def read_cmd(buf):
	print("read_cmd(pos=%x)" % buf.pos)
	pos = buf.pos
	while True:
		context.decoded[buf.pos] = 1
		cmd = buf.read_b()
		if cmd != 0:
			break
	
	print("cmd=%x" % cmd)

	if cmd in [0x10, 0x14, 0x15, 0x16, 0x17]:
		goto = buf.read_l()
		context.candidates.add(goto)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tGOTO %x" % (pos, goto)

	elif cmd == 0x11:
		goto = buf.read_l()
		context.candidates.add(goto)
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tIF %s GOTO %x" % (pos, ", ".join(params), goto)

	elif cmd == 0x18:
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return False, "%X:\tGOTO (%s)" % (pos, ", ".join(params))

	elif cmd == 0x20:
		offset = buf.read_w()
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\t(0xff00e6, 0x%x).bit = %s" % (pos, offset, ", ".join(params))

	elif cmd == 0x21:
		offset = buf.read_w()
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\t(0xff01e6, 0x%x).b = %s" % (pos, offset, ", ".join(params))

	elif cmd == 0x22:
		offset = buf.read_w()
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\t(0xff03e6, 0x%x).w = %s" % (pos, offset, ", ".join(params))

	elif cmd == 0x23:
		offset = buf.read_b()
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\t(0xff07e6, 0x%x).l = %s" % (pos, offset, ", ".join(params))

	elif cmd == 0x28:
		var_id = buf.read_b()
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tVAR_A6[%d] = %s" % (pos, var_id, ", ".join(params))

	elif cmd == 0x29:
		var_id = buf.read_b()
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tVAR_B6[%d] = %s" % (pos, var_id, ", ".join(params))

	elif cmd == 0x2a:
		var_id = buf.read_b()
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tVAR_C6[%d] = %s" % (pos, var_id, ", ".join(params))

	elif cmd == 0x2b:
		var_id = buf.read_b()
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tVAR_D6[%d] = %s" % (pos, var_id, ", ".join(params))

	elif cmd == 0x2c:
		var_id = buf.read_b()
		sub_var_id = read_params(buf)
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tVAR_A6[%d, %s] = %s" % (pos, var_id, sub_var_id, ", ".join(params))

	elif cmd == 0x2d:
		var_id = buf.read_b()
		sub_var_id = read_params(buf)
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tVAR_B6[%d, %s] = %s" % (pos, var_id, sub_var_id, ", ".join(params))

	elif cmd == 0x2e:
		var_id = buf.read_b()
		sub_var_id = read_params(buf)
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tVAR_C6[%d, %s] = %s" % (pos, var_id, sub_var_id, ", ".join(params))

	elif cmd == 0x2f:
		var_id = buf.read_b()
		sub_var_id = read_params(buf)
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tVAR_D6[%d, %s] = %s" % (pos, var_id, sub_var_id, ", ".join(params))

	elif cmd == 0x40:
		ptr_cmd = buf.read_l()
		context.candidates.add(ptr_cmd)
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tGOSUB %x(%s)" % (pos, ptr_cmd, ", ".join(params))
		
	elif cmd == 0x41:
		ptr_fun = buf.read_l()
		context.functions.add(ptr_fun)
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tfun_%x(%s)" % (pos, ptr_fun, ", ".join(params))

	elif cmd == 0x50:
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tWRITE_STRUCT_4(%s)" % (pos, ", ".join(params))

	elif cmd == 0x51:
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tWRITE_STRUCT_5(%s)" % (pos, ", ".join(params))
				
	elif cmd == 0x52:
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tWRITE_STRUCT_6(%s)" % (pos, ", ".join(params))
				
	elif cmd == 0x53:
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tWRITE_STRUCT_7(%s)" % (pos, ", ".join(params))
				
	elif cmd == 0x54:
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tWRITE_STRUCT_8(%s)" % (pos, ", ".join(params))
				
	elif cmd == 0x55:
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tWRITE_STRUCT_A(%s)" % (pos, ", ".join(params))
				
	elif cmd == 0x56:
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tWRITE_STRUCT_C(%s)" % (pos, ", ".join(params))
				
	elif cmd == 0x57:
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tWRITE_STRUCT_E(%s)" % (pos, ", ".join(params))
				
	elif cmd == 0x58:
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tWRITE_STRUCT_10(%s)" % (pos, ", ".join(params))
				
	elif cmd == 0x59:
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tWRITE_STRUCT_14(%s)" % (pos, ", ".join(params))
				
	elif cmd == 0x5a:
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tWRITE_STRUCT_18(%s)" % (pos, ", ".join(params))
				
	elif cmd == 0x5b:
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tWRITE_STRUCT_1C(%s)" % (pos, ", ".join(params))
				
	elif cmd == 0x5c:
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tWRITE_20(%s)" % (pos, ", ".join(params))

	elif cmd == 0x5d:
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tWRITE_24(%s)" % (pos, ", ".join(params))

	elif cmd == 0x5e:
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tWRITE_28(%s)" % (pos, ", ".join(params))

	elif cmd == 0x5f:
		params = read_params(buf)
		print("/read_cmd(pos=%x)" % buf.pos)
		return True, "%X:\tWRITE_2C(%s)" % (pos, ", ".join(params))

	elif cmd == 0xff:
		print("/read_cmd(pos=%x)" % buf.pos)
		return False, "%X:\tRETURN" % (pos,)

	else:
		return False, "%X:\tILLEGAL" % (pos,)

def read_params(buf):
	print("read_params(pos=%x)" % buf.pos)
	if buf.read_b(buf.pos) == 0xf1:
		buf.read_b()
		return []
	params = [read_value(buf)]
	while True:
		sep = source.read_b()
		print("sep=%x" % sep)
		if sep == 0xf0:
			params.append(read_value(buf))
		elif sep == 0xf1:
			print("/read_params(pos=%x)" % buf.pos)
			return params

def read_value(buf):
	print("read_param(pos=%x)" % buf.pos)
	while True:
		val = buf.read_b()
		if val != 0:
			break
	
	print("val=%x" % val)
	if val == 0x20:
		offset = buf.read_w()
		res = "(0xff00e6, 0x%x).bit" % offset

	elif val == 0x21:
		offset = buf.read_w()
		res = "(0xff01e6, 0x%x)" % offset

	elif val == 0x22:
		offset = buf.read_w()
		res = "(0xff03e6, 0x%x)" % (2*offset)

	elif val == 0x23:
		offset = buf.read_b()
		res = "(0xff07e6, 0x%x)" % (4*offset)

	elif val == 0x28:
		var_id = buf.read_b()
		res = "VAR_A6[%d]" % var_id

	elif val == 0x29:
		var_id = buf.read_b()
		res = "VAR_B6[%d]" % var_id

	elif val == 0x2a:
		var_id = buf.read_b()
		res = "VAR_C6[%d]" % var_id

	elif val == 0x2b:
		var_id = buf.read_b()
		res = "VAR_D6[%d]" % var_id

	elif val == 0x2c:
		var_id = buf.read_b()
		params = read_params(buf)
		res = "VAR_A6[%d, %s]" % (var_id, ", ".join(params))

	elif val == 0x2d:
		var_id = buf.read_b()
		params = read_params(buf)
		res = "VAR_B6[%d, %s]" % (var_id, ", ".join(params))

	elif val == 0x2e:
		var_id = buf.read_b()
		params = read_params(buf)
		res = "VAR_C6[%d, %s]" % (var_id, ", ".join(params))

	elif val == 0x2f:
		var_id = buf.read_b()
		params = read_params(buf)
		res = "VAR_D6[%d, %s]" % (var_id, ", ".join(params))

	elif val == 0x40:
		ptr_cmd = buf.read_l()
		context.candidates.add(ptr_cmd)
		params = read_params(buf)
		res = "GOSUB %x (%s)" % (ptr_cmd, ", ".join(params))

	elif val == 0x41:
		ptr_fun = buf.read_l()
		context.functions.add(ptr_fun)
		params = read_params(buf)
		res = "fun_%x(%s)" % (ptr_fun, ", ".join(params))

	elif val == 0x50:
		res = "READ_04()"

	elif val == 0x51:
		res = "READ_05()"

	elif val == 0x52:
		res = "READ_06()"

	elif val == 0x53:
		res = "READ_07()"

	elif val == 0x54:
		res = "READ_08()"

	elif val == 0x55:
		res = "READ_0A()"

	elif val == 0x56:
		res = "READ_0C()"

	elif val == 0x57:
		res = "READ_0E()"

	elif val == 0x58:
		res = "READ_10()"

	elif val == 0x59:
		res = "READ_14()"

	elif val == 0x5a:
		res = "READ_18()"

	elif val == 0x5b:
		res = "READ_1C()"

	elif val == 0x5c:
		res = "READ_20()"

	elif val == 0x5d:
		res = "READ_24()"

	elif val == 0x5e:
		res = "READ_28()"

	elif val == 0x5f:
		res = "READ_2C()"

	elif val == 0xa0:
		res = "0x%x" % buf.read_b()

	elif val == 0xa1:
		res = "0x%x" % buf.read_w()

	elif val == 0xa2:
		data = buf.read_l()
		context.data.add(data)
		res = "0x%x" % data
		
	elif val == 0xaf:
		parenthesed_expr = read_value(buf)
		res = "(%s)" % parenthesed_expr
		if buf.read_b() != 0xf1:
			raise Exception("[f1] expected at 0x%x" % (buf.pos - 1))

	elif val == 0xc4:
		parenthesed_expr = read_value(buf)
		res = "not(%s)" % parenthesed_expr

	elif val == 0xc5:
		parenthesed_expr = read_value(buf)
		res = "-(%s)" % parenthesed_expr

	elif val == 0xf0:
		warns("Strange [f0] terminator at %x" % (buf.pos - 1))
		res = ""
		buf.pos -= 1

	elif val == 0xf1:
		warns("Strange [f1] terminator at %x" % (buf.pos - 1))
		res = ""
		buf.pos -= 1
	
	else:
		warns("Unknown value [%02x]" % val)
		res = "<illegal>"
		
	print("res=%s" % res)
	while True:
		next_token = source.read_b(source.pos)
		print("next_token=%x" % next_token)
		if next_token == 0xf0 or next_token == 0xf1:
#			source.pos += 1
			print("/read_param(pos=%x)" % buf.pos)
			return res
		else:
			res += read_right_expr(buf)
	return res


def read_right_expr(buf):
	print("read_right_expr(pos=%x)" % buf.pos)
	op = source.read_b()
	print("op=%x" % op)
	
	if op == 0xc8:
		right = read_value(buf)
		print("/read_right_expr(pos=%x)" % buf.pos)
		return "*" + right

	if op == 0xc9:
		right = read_value(buf)
		print("/read_right_expr(pos=%x)" % buf.pos)
		return "/" + right

	if op == 0xca:
		right = read_value(buf)
		print("/read_right_expr(pos=%x)" % buf.pos)
		return "%" + right

	elif op == 0xcc:
		right = read_value(buf)
		print("/read_right_expr(pos=%x)" % buf.pos)
		return " + " + right
	
	elif op == 0xcd:
		right = read_value(buf)
		print("/read_right_expr(pos=%x)" % buf.pos)
		return " - " + right

	elif op == 0xd0:
		right = read_value(buf)
		print("/read_right_expr(pos=%x)" % buf.pos)
		return " <? " + right

	elif op == 0xd1:
		right = read_value(buf)
		print("/read_right_expr(pos=%x)" % buf.pos)
		return " <=? " + right

	elif op == 0xd2:
		right = read_value(buf)
		print("/read_right_expr(pos=%x)" % buf.pos)
		return " >? " + right

	elif op == 0xd3:
		right = read_value(buf)
		print("/read_right_expr(pos=%x)" % buf.pos)
		return " >=? " + right

	elif op == 0xd4:
		right = read_value(buf)
		print("/read_right_expr(pos=%x)" % buf.pos)
		return " == " + right

	elif op == 0xd5:
		right = read_value(buf)
		print("/read_right_expr(pos=%x)" % buf.pos)
		return " != " + right
	
	elif op == 0xd8:
		right = read_value(buf)
		print("/read_right_expr(pos=%x)" % buf.pos)
		return " & " + right

	elif op == 0xe0:
		right = read_value(buf)
		print("/read_right_expr(pos=%x)" % buf.pos)
		return " | " + right

	elif op == 0xf0 or op == 0xf1:
		print("/read_right_expr(pos=%x)" % buf.pos)
		buf.pos -= 1
		return ""
	
	else:
		warns("Unknown operator [%02x]" % op)
		return " ? "


def decompile(buf, res=[]):
	running = True
	
	context.dialogs = []
	while running:
		last_cmd = ""
		while True:
			pos = buf.pos
			cont, line = read_cmd(source)
			res.append((pos, line))
			if not cont: 
				break
			last_cmd = line
		
		res.append((buf.pos, ""))
#		print("\n".join(res))
		
		print("candidates for code:")
		for pos in context.candidates:
			print("\t%x" % pos)
		
		print("\nfunctions:")
		for pos in context.functions:
			print("\t%x" % pos)
		
		while True:
			if len(context.candidates) == 0:
				running = False
				break
			else:
				pos = context.candidates.pop()
				if pos < len(context.decoded) and context.decoded[pos] == 0:
					source.set_pos(pos)
					break
	return res

source.set_pos(0xa97f)
res = decompile(source)
source.set_pos(0x12b16)
res = decompile(source, res)
source.set_pos(0x6531c)
res = decompile(source, res)
source.set_pos(0xdf45)
res = decompile(source, res)

source.set_pos(0x322de)
res = decompile(source, res)
source.set_pos(0x324ff)
res = decompile(source, res)
source.set_pos(0x3257a)
res = decompile(source, res)
source.set_pos(0x32c58)
res = decompile(source, res)
source.set_pos(0x32d6a)
res = decompile(source, res)
source.set_pos(0x32e54)
res = decompile(source, res)
source.set_pos(0x33f14)
res = decompile(source, res)
source.set_pos(0x37a8a)
res = decompile(source, res)




res.sort(key=lambda line: line[0])

context.dialogs = []
old_line = (0, "")
last_cmd = ""
with open("decomp.txt", "w") as f:
	for line in res:
		if old_line != line:
			f.write(line[1])
			f.write("\n")
			if "ILLEGAL" in line[1] and "GOTO" in last_cmd:
				context.dialogs.append(line[0])
			last_cmd = line[1]
		old_line = line
	
	f.write("\n\n")
	f.write("candidates for code:\n")
	for pos in context.candidates:
		f.write("\t%x\n" % pos)
	
	f.write("candidates for data:\n")
	for pos in context.data:
		f.write("\t%x\n" % pos)
	
with open("ptr_to_dialogs.txt", "w") as f:
	for pos in context.dialogs:
		f.write("0x%x\n" % pos)
