# -*- coding: utf-8 -*-


from buffer import Buffer
# from utils import load_from_png8, save_png8, TileSet, surface_to_tilemap
import numpy as np
import os

np.set_printoptions(formatter={'int':hex})
verbose = False
warnings=[]

def warns(warning):
	warnings.append(warning)

def print_warnings():
	for warning in warnings:
		print(warning)

source = Buffer.load("bin/Surging Aura (Japan).md")


source.set_size(0x300000)
source.set_pos(0x210000)
symbols = {}

def get_tag(line, tag):
	i = line.index(tag)
	j = line.index("=", i + len(tag))
	if "," in line[j:]:
		k = line.index(",", j + 1)
	else:
		k = len(line)
	print(i, j, k, line[i:j], line[j:k])
	return line[j + 1 : k].strip()
	

def load_script(res, path):
	with open(path, encoding="utf8") as f:
		lines = f.readlines()
	
	i = 0
	pos = -1
	text = []
	width = height = -1

	while i < len(lines):
		while i < len(lines):
			line = lines[i].strip()
			if not line.startswith(";"):
				break
#			print(i, "comment:", line)

			if "pos=" in line:
				pos = int(get_tag(line, "pos"), 16)
			if "width=" in line:
				width = int(get_tag(line, "width"))
			if "height=" in line:
				height = int(get_tag(line, "height"))
			i += 1
		
		while i < len(lines):
			line = lines[i].rstrip()
			if line == "":
				if pos in res:
					print("text at 0x%x alreay defined" % pos)
				else:
					if height == -1:
						res[pos] = {"text": "[0d]".join(text), "pos": pos, "width": width, "height": height}
					else:
						res[pos] = {"text": "\n".join(text), "pos": pos, "width": width, "height": height}
				pos = -1
				text = []
				width = height = -1
				break
#			print(i, "text:", line)
			text.append(line)
			i += 1

		while i < len(lines):
			line = lines[i].strip()
#			print(i, "blank:", line)
			if line != "":
				break
			i += 1
	return res

script = {}
load_script(script, "test-script.txt")

encoding = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[¥]^_`abcdefghijklmnopqrstuvwxyz{|}"""



for pos in script:
	text_pos = source.pos
	
	source.write_b(0x10, pos=pos)
	source.write_l(text_pos, pos=pos+1)

	line = script[pos]
	text = line["text"]
	
	i = 0
	ignore_cr = False
	while i < len(text):
		c = text[i]
		i += 1
		if c == "[":
			j = i
			while i < len(text):
				c = text[i]
				i += 1
				if c == "]": 
					break
			tag = text[j : i-1]
			print(tag)
		
			if tag == "00":
				source.write_b(0)
			
			elif tag == "01":
				source.write_b(0x01)

			elif tag == "02":
				source.write_b(0x02)

			elif tag == "0d":
				if not ignore_cr:
					source.write_b(0x0d)
			
			elif tag == "wait":
				source.write_b(0x09)
				ignore_cr = True
			
			elif tag == "clear":
				source.write_b(0x0c)
				ignore_cr = True
	
			elif tag == "Mu":
				source.write_b(0x0a)
			
			else:
				raise Exception("%X: unknown tag: [%s]" % (pos, tag))
		
		else:
			ignore_cr = False
			if c not in encoding:
				raise Exception("%X: Unknown char: [%s]" % (pos, c))
			source.write_b(0x20 + encoding.index(c))


source.write_text("Mu\x00", pos=0x13646)

source.align()
symbols["hackStart"] = source.pos

source.include("asm/hack.asm", symbols)

source.save("bin/out.bin")
	
		
	
	
	
	
	