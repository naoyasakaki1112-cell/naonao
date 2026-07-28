from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "concepts"
OUT = ROOT / "output" / "concepts"
OUT.mkdir(parents=True, exist_ok=True)

FONT_SANS = Path(r"C:\Windows\Fonts\NotoSansJP-VF.ttf")
FONT_SERIF = Path(r"C:\Windows\Fonts\NotoSerifJP-VF.ttf")


def font(path, size):
    return ImageFont.truetype(str(path), size=size)


SANS = FONT_SANS
SERIF = FONT_SERIF

INK = "#18211e"
MUTED = "#647067"
PAPER = "#f7f4ed"
WHITE = "#fffdf8"
CHARCOAL = "#26302b"
MOSS = "#475f4c"
CEDAR = "#8a603d"
LINE = "#d7ddd3"


def fit_cover(img, size):
    img = ImageOps.exif_transpose(img.convert("RGB"))
    return ImageOps.fit(img, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def rounded_rectangle(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def wrap_text(draw, text, font_obj, max_width):
    lines = []
    current = ""
    for char in text:
        candidate = current + char
        if draw.textlength(candidate, font=font_obj) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = char
    if current:
        lines.append(current)
    return lines


def draw_text_block(draw, text, xy, font_obj, fill, max_width, line_gap=8):
    x, y = xy
    lines = wrap_text(draw, text, font_obj, max_width)
    for line in lines:
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += font_obj.size + line_gap
    return y


def draw_chip(draw, text, xy, fill, text_fill=WHITE):
    x, y = xy
    f = font(SANS, 22)
    pad_x, pad_y = 18, 8
    w = int(draw.textlength(text, font=f) + pad_x * 2)
    h = f.size + pad_y * 2
    rounded_rectangle(draw, (x, y, x + w, y + h), 18, fill=fill)
    draw.text((x + pad_x, y + pad_y - 2), text, font=f, fill=text_fill)
    return x + w + 10


def create_board(spec):
    W, H = 1600, 1000
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    hero = fit_cover(Image.open(ASSETS / spec["image"]), (900, 1000))
    img.paste(hero, (700, 0))
    overlay = Image.new("RGBA", (900, 1000), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((0, 0, 260, 1000), fill=(247, 244, 237, 230))
    od.rectangle((260, 0, 900, 1000), fill=(0, 0, 0, spec["hero_overlay"]))
    img.paste(overlay, (700, 0), overlay)
    draw = ImageDraw.Draw(img)

    draw.text((70, 62), "YOHAKU CONCEPT", font=font(SANS, 24), fill=CEDAR)
    draw.ellipse((70, 112, 122, 164), fill=CHARCOAL)
    draw.text((88, 121), "余", font=font(SERIF, 28), fill=WHITE)
    draw.text((140, 116), spec["brand"], font=font(SANS, 34), fill=INK)

    draw.text((70, 205), spec["name"], font=font(SERIF, 74), fill=INK)
    draw.text((70, 292), spec["kana"], font=font(SANS, 27), fill=CEDAR)
    draw_text_block(draw, spec["concept"], (70, 350), font(SANS, 30), INK, 560, line_gap=12)

    chip_y = 510
    x = 70
    for chip in spec["chips"]:
        x = draw_chip(draw, chip, (x, chip_y), spec["accent"])
        if x > 540:
            x = 70
            chip_y += 56

    rounded_rectangle(draw, (70, 640, 630, 898), 22, fill=WHITE, outline=LINE, width=2)
    draw.text((104, 674), "想定用途", font=font(SANS, 28), fill=INK)
    y = 728
    for item in spec["uses"]:
        draw.text((104, y), "・" + item, font=font(SANS, 23), fill=MUTED)
        y += 42

    rounded_rectangle(draw, (730, 660, 1518, 880), 24, fill=(255, 253, 248), outline=None)
    draw.text((770, 694), spec["scene_title"], font=font(SANS, 27), fill=INK)
    draw_text_block(draw, spec["scene_copy"], (770, 748), font(SANS, 24), MUTED, 660, line_gap=10)

    draw.text((70, 930), spec["notes"], font=font(SANS, 23), fill=CEDAR)
    draw.text((1270, 930), "LIMITED 108", font=font(SANS, 28), fill=WHITE)

    out_path = OUT / spec["out"]
    img.save(out_path, quality=95)
    return out_path


SPECS = [
    {
        "image": "parents-gift.png",
        "out": "concept-01-oyakoukou-shizuka.png",
        "brand": "YOHAKU / 余白香",
        "name": "親孝香",
        "kana": "OYAKOUKOU - 静かな親孝行を贈る香り",
        "concept": "落ち着いた静寂を好む両親へ。ホテルの華やかさではなく、実家の玄関や寝室にそっと馴染む、寺の朝のようなやさしい余白。",
        "chips": ["両親ギフト", "寝室", "玄関", "長寿祝い"],
        "uses": ["母の日・父の日・敬老の日の上質ギフト", "静かな暮らしを好む両親の寝室や書斎", "香りが強すぎるものが苦手な家庭向け"],
        "scene_title": "贈る相手の暮らしに、静けさを。",
        "scene_copy": "華やかさよりも落ち着きを大切にする両親へ。強く香らせるのではなく、玄関や寝室に入った瞬間の空気をそっと整えるギフト。",
        "notes": "香調: 檜 / 白檀 / 柚子 / ほうじ茶",
        "accent": CEDAR,
        "hero_overlay": 20,
    },
    {
        "image": "vip-hospitality.png",
        "out": "concept-02-rinka-vip.png",
        "brand": "YOHAKU / 余白香",
        "name": "凛香",
        "kana": "RINKA - もてなしの余韻を残す香り",
        "concept": "和の飲食店、クリニック、美容サロンの上顧客ギフトへ。清潔感と品格を両立し、施術や食事のあとに記憶として残る静かな贈り物。",
        "chips": ["和の飲食店", "美容サロン", "クリニック", "VIPギフト"],
        "uses": ["会員制和食店・鮨店の手土産", "美容サロンの上顧客向けギフト", "クリニックの開院祝い・VIP紹介礼品"],
        "scene_title": "上顧客の記憶に残る、静かな手土産。",
        "scene_copy": "和食店、クリニック、美容サロンの空間になじむ清潔感。施術や食事の余韻を、自宅に持ち帰れる上質なギフトとして。",
        "notes": "香調: 白檀 / 緑茶 / 柚子皮 / ムスク",
        "accent": MOSS,
        "hero_overlay": 18,
    },
    {
        "image": "luxury-bedroom.png",
        "out": "concept-03-tsukiji-6am.png",
        "brand": "YOHAKU / 余白香",
        "name": "築地、午前六時",
        "kana": "TSUKIJI 6AM - 都心の寝室に戻る静寂",
        "concept": "富裕層の寝室や湾岸タワーマンションへ。都市の明かりを遠くに、眠る前の空間を寺の朝のように整える。",
        "chips": ["富裕層寝室", "湾岸住戸", "移転祝い", "成約ギフト"],
        "uses": ["湾岸タワーマンションの寝室・書斎", "不動産成約祝い・入居祝い", "経営者や投資家へのプライベートギフト"],
        "scene_title": "都心の寝室に、朝のお堂の余白を。",
        "scene_copy": "湾岸の高層住戸や経営者の寝室へ。都市の明かりを遠くに感じながら、眠る前の空間を静かに切り替える一本。",
        "notes": "香調: 檜 / 沈香ニュアンス / ベチバー / 茶",
        "accent": CHARCOAL,
        "hero_overlay": 6,
    },
]


def main():
    for spec in SPECS:
        print(create_board(spec))


if __name__ == "__main__":
    main()
