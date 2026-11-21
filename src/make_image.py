import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 768
PAPER = (246, 241, 227)
NAVY = (29, 53, 87)
INK = (20, 33, 61)
GREY = (107, 114, 128)
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

# guilloche: faint sine waves over the whole spread
for base in range(-40, H + 40, 26):
    pts = [(x, base + 7 * math.sin(x / 46.0 + base)) for x in range(0, W + 8, 8)]
    d.line(pts, fill=(120, 145, 175, 26), width=1)
# page seam
for i in range(26):
    a = int(70 * (1 - i / 26))
    d.line([(512 - 26 + i, 0), (512 - 26 + i, H)], fill=(90, 80, 60, a))
    d.line([(512 + i, 0), (512 + i, H)], fill=(255, 255, 255, a // 2))

def text(x, y, s, font, size, fill=INK, anchor="la"):
    d.text((x, y), s, font=ImageFont.truetype(font, size), fill=fill, anchor=anchor)

# ---------- LEFT PAGE: data page ----------
text(118, 40, "REPUBLIC OF VESSARA", SERIF_B, 29, NAVY)
text(118, 78, "PASSEPORT · PASSPORT", SANS, 13, GREY)
# emblem: circle with waves and a star
d.ellipse([52, 34, 106, 88], outline=NAVY, width=2)
for k in range(3):
    yy = 56 + k * 9
    pts = [(58 + t, yy + 2.5 * math.sin(t / 6.0)) for t in range(0, 43, 3)]
    d.line(pts, fill=NAVY, width=1)
text(79, 40, "★", SANS, 13, NAVY, anchor="ma")
d.line([(40, 108), (492, 108)], fill=NAVY, width=2)

# photo
px, py, pw, ph = 48, 138, 148, 188
d.rectangle([px, py, px + pw, py + ph], fill=(203, 213, 220), outline=NAVY, width=2)
for t in range(-ph, pw, 14):
    d.line([(px + t, py + ph), (px + t + ph, py)], fill=(255, 255, 255, 60), width=3)
# portrait silhouette
d.ellipse([px + 44, py + 34, px + 104, py + 100], fill=(84, 99, 114))
d.pieslice([px + 22, py + 96, px + 126, py + 196], 180, 360, fill=(84, 99, 114))
d.rectangle([px, py + ph - 22, px + pw, py + ph], fill=(29, 53, 87, 200))
text(px + pw // 2, py + ph - 20, "ALMAR · T.", SANS_B, 12, (255, 255, 255), anchor="ma")

def field(x, y, label, value, vsize=16):
    text(x, y, label, SANS, 10, GREY)
    text(x, y + 13, value, SANS_B, vsize, INK)

field(216, 138, "TYPE / TYPE", "P")
field(300, 138, "CODE / CODE", "VSR")
field(392, 138, "PASSPORT Nº", "VSR-0482137", 15)
field(216, 186, "SURNAME / NOM", "ALMAR", 19)
field(216, 232, "GIVEN NAMES / PRÉNOMS", "TOMAS ILEN", 17)
field(216, 278, "NATIONALITY / NATIONALITÉ", "VESSARAN")
field(48, 344, "DATE OF BIRTH / DATE DE NAISSANCE", "14 MAR 1989")
field(300, 344, "SEX / SEXE", "M")
field(48, 392, "PLACE OF BIRTH / LIEU DE NAISSANCE", "PORT ALMARA")
field(48, 440, "DATE OF ISSUE / DATE DE DÉLIVRANCE", "03 JUN 2021")
field(300, 440, "EXPIRY / DATE D'EXPIRATION", "03 JUN 2031")
field(48, 488, "AUTHORITY / AUTORITÉ", "DELTA OFFICE — PORT ALMARA")
text(48, 548, "Holder's signature / Signature du titulaire:", SANS, 10, GREY)
text(48, 566, "T. Almar", SERIF_B, 20, (40, 50, 90))
text(48, 606, "This passport contains 32 pages · Ce passeport contient 32 pages", SANS, 10, GREY)
# MRZ
mrz1 = "P<VSRALMAR<<TOMAS<ILEN".ljust(44, "<")
mrz2 = "VSR0482137<4VSR8903145M3106032".ljust(43, "<") + "8"
d.rectangle([40, 668, 492, 736], fill=(255, 255, 255, 90))
text(48, 678, mrz1, MONO, 16, INK)
text(48, 704, mrz2, MONO, 16, INK)

# ---------- RIGHT PAGE: visas ----------
text(552, 40, "VISAS", SERIF_B, 24, NAVY)
text(552, 74, "VISAS · VISA", SANS, 12, GREY)
d.line([(532, 108), (984, 108)], fill=NAVY, width=2)

def stamp(w, h, draw_fn):
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    draw_fn(ld, w, h)
    return layer

def paste(layer, cx, cy, angle):
    r = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(r, (cx - r.width // 2, cy - r.height // 2), r)

INDIGO = (51, 65, 140, 215)
def kharad(ld, w, h):
    ld.rounded_rectangle([4, 4, w - 4, h - 4], 10, outline=INDIGO, width=4)
    ld.rounded_rectangle([12, 12, w - 12, h - 12], 7, outline=INDIGO, width=1)
    f1 = ImageFont.truetype(SANS_B, 24); f2 = ImageFont.truetype(SANS, 15); f3 = ImageFont.truetype(SANS_B, 19)
    ld.text((w // 2, 16), "KHARAD", font=f1, fill=INDIGO, anchor="ma")
    ld.text((w // 2, 50), "PORT OF SEL — ARRIVED", font=f2, fill=INDIGO, anchor="ma")
    ld.text((w // 2, 74), "18 JUL 2022", font=f3, fill=INDIGO, anchor="ma")
paste(stamp(264, 116, kharad), 668, 190, -6)

CRIMSON = (157, 44, 44, 215)
def solmire(ld, w, h):
    ld.ellipse([4, 4, w - 4, h - 4], outline=CRIMSON, width=4)
    ld.ellipse([14, 14, w - 14, h - 14], outline=CRIMSON, width=1)
    f1 = ImageFont.truetype(SANS_B, 21); f2 = ImageFont.truetype(SANS, 14); f3 = ImageFont.truetype(SANS_B, 16)
    ld.text((w // 2, 38), "SOLMIRE", font=f1, fill=CRIMSON, anchor="ma")
    ld.text((w // 2, 68), "DEPARTED", font=f2, fill=CRIMSON, anchor="ma")
    ld.text((w // 2, 88), "02 AUG 2022", font=f3, fill=CRIMSON, anchor="ma")
    ld.text((w // 2, 114), "GATE 3", font=f2, fill=CRIMSON, anchor="ma")
paste(stamp(176, 176, solmire), 872, 330, 5)

TEAL = (15, 118, 110, 215)
def vessara(ld, w, h):
    ld.rounded_rectangle([4, 4, w - 4, h - 4], 10, outline=TEAL, width=4)
    f1 = ImageFont.truetype(SANS_B, 16); f2 = ImageFont.truetype(SANS_B, 18)
    ld.text((w // 2, 10), "PORT ALMARA", font=f1, fill=TEAL, anchor="ma")
    ld.text((w // 2, 33), "FERRY TERMINAL — ARRIVED", font=f1, fill=TEAL, anchor="ma")
    ld.text((w // 2, 62), "09 MAY 2023", font=f2, fill=TEAL, anchor="ma")
paste(stamp(272, 108, vessara), 724, 428, 3)

BROWN = (124, 74, 33, 220)
def tide(ld, w, h):
    ld.rectangle([3, 3, w - 3, h - 3], outline=BROWN, width=3)
    f1 = ImageFont.truetype(SANS_B, 16); f2 = ImageFont.truetype(SANS, 13)
    ld.text((w // 2, 12), "TIDE TABLES CARRIED ✓", font=f1, fill=BROWN, anchor="ma")
    ld.text((w // 2, 40), "HARBOUR ACT §12 — FERRY FEE PAID", font=f2, fill=BROWN, anchor="ma")
paste(stamp(316, 72, tide), 742, 580, -3)

text(552, 700, "Endorsements / Mentions: see page 4", SANS, 11, GREY)

img.save("/home/hatch/workspace/makefun/bots/vessara-passport/entry.png")
print("saved")
