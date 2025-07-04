# -*- coding: utf-8 -*-

from buffer import Buffer
import numpy as np
import png

def save_png8(surf, palette, path):
	height, width = surf.shape
	w = png.Writer(width, height, palette=palette, bitdepth=8)
	with open(path, 'wb') as f:
		w.write(f, surf)

palette = [
	(0, 0, 0), (0, 0, 255), (0, 255, 0), (0, 255, 255), (255, 0, 0), (255, 0, 255), (255, 255, 0), (255, 255, 255), 
	(128, 128, 128), (0, 0, 128), (0, 128, 0), (0, 128, 128), (128, 0, 0), (128, 0, 128), (128, 128, 0), (192, 192, 192)
]*8



source = Buffer.load("bin/Surging Aura (Japan).md")

if True:
	source.set_pos(0xb4100)
	
	delta = 20
	width, height = 400, 280
	res = np.zeros((height, width), dtype=np.uint8)
	
	fg_color = 7
	bg_color = 0
	x0 = y0 = 0
	for i in range(272):
		print("char 0x%x at 0x%x" % (i, source.pos))
		for y in range(16):
			data = source.read_b()
	#		print("t: %02x" % data)
			for x in range(8):
				if data & 1:
					res[y0 + y, x0 + 7 - x] = fg_color
				else:
					res[y0 + y, x0 + 7 - x] = bg_color
				data = data >> 1
		if False:
			for y in range(16):
				data = source.read_b()
		#		print("b: %02x" % data)
				for x in range(8):
					if data & 1:
						res[y0 + y, x0 + 15 - x] = fg_color
					else:
						res[y0 + y, x0 + 15 - x] = bg_color
					data = data >> 1
		x0 += delta
		if x0 >= width:
			x0 = 0
			y0 += delta
	
	save_png8(res, palette, "font.png")


encoding_d5378 = """愛悪安闇衣遣域運衛炎王屋下家会壊海界外活官間気義救強恐軍擊結月剣建見軒鍵古光口広港行国婚魂座砦罪殺使士姉子師死紙時式疾者邪守手酒呪周襲宿出所女勝将小城場心神臣身人水世正生精聖跡說宣戦想装像賊退代大男知地中仲町長撤典天伝東逃動道日入年配買泊発妃備姫父負部風復物兵平宝法北魔妹娘名命滅目勇理旅力老和話『』「」《》放後盗船渡金元親失抱少修航牢声怒姿獄気防御護々扉⁉‼攻µµµµµµµµ青龍刀波鮮斬曲刃丸白狼輝止切幻斧鬼紫鎚爆裂棒杖弓明吠翔槍爪布服皮鎧鉄赤招帽木楯破指輪幸腕空胸飾符套売右雨何火向左山事上西村南方薬様用石竜牙雷太陽真紅鉛鋼茨硬革騎仮面全快書固液念属性岬舞五玉敗決着詠唱体味方敵逆回復補助思陰状態髮貴私僧期待片腹痛希望形消再来突專短持両半重幅帯銳能昇速度特定確率避無遠距離可武器円秘謎軽量堅作同付込高削除象徵脱巻病治不闘記念兜塔最具前呼未奥集野言祝砲母化新"""

encoding_b850c = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[¥]^_`abcdefghijklmnopqrstuvwxyz{|}¤¤ぁあいいううぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびびふぶぷへべぺほぼぼまみむめもゃやゅゆょよらりるれろわわ♡☆をん¤。、・µァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプへベペホボポマミムメモャヤュユョヨラリルレロワワ♡☆ヲンヴ。、・µ"""


def get_text(buf):
	katakana = False
	
	res = ""
	is_text = False
	while True:
		val = buf.read_b()
		print("[%02x]" % val)
		
		if val == 0:
			res += "[00]"
			break
	
		elif val & 0xf0 == 0xf0:
			val = ((val & 0xf) << 8) + buf.read_b()
			if val >= len(encoding_d5378):
				print("03: unrecognized [%03x]" % val)
				return
			res += encoding_d5378[val]
		
		elif val == 0x01:
			res += "[01]"

		elif val == 0x02:
			res += "[02]"

		elif val == 0x03:
			katakana = False
	
		elif val == 0x04:
			katakana = True
	
		elif val == 0x05:
			a = buf.read_b()
			b = buf.read_b()
			res += "[05, %02x, %02x]" % (a, b)

		elif val == 0x06:
			a = buf.read_b()
			res += "[06, %02x]" % a

		elif val == 0x07:
			a = buf.read_b()
			res += "[07, %02x]" % a

		elif val == 0x08:
			a = buf.read_b()
			res += "[08, %02x]" % a

		elif val == 0x09:
			res += "[wait]"
	
		elif val == 0x0a:
			res += "[ムウ]"
	
		elif val == 0x0b:
			a = buf.read_b()
			res += "[0b, %02x]" % a

		elif val == 0x0c:
			res += "[clear]\n"
	
		elif val == 0x0d:
			res += "\n"
			
		elif val == 0x0e:
			continue

		elif val == 0x0f:
			continue

		elif val >= 0x60:
			is_text = True
			if katakana:
				val += 88
			if val >= len(encoding_b850c):
				print("02: unrecognized [%02x]" % val)
				return
			res += encoding_b850c[val]
	
		elif val >= 0x20:
			is_text = True
			res += encoding_b850c[val - 0x20]
		
		else:
			print("01: unrecognized [%02x]" % val)
			return
	
	if is_text:
		return res
		
with open("ptr_to_dialogs.txt") as f:
	ptrs = [int(line, 16) for line in f.readlines()]

res = []
for pos in ptrs:
	print("%x:" % pos)
	source.set_pos(pos)
	txt = get_text(source)
	if txt:
		res.append("; pos=0x%x\n%s\n" % (pos, txt))

print("\n".join(res))

with open("script.txt", "w", encoding="utf-8") as f:
	f.write("\n".join(res))
