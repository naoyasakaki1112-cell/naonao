from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUT = ROOT / "output" / "lp"
OUT.mkdir(parents=True, exist_ok=True)

FONT_SANS = Path(r"C:\Windows\Fonts\NotoSansJP-VF.ttf")
FONT_SERIF = Path(r"C:\Windows\Fonts\NotoSerifJP-VF.ttf")

INK = "#18211e"
MUTED = "#647067"
PAPER = "#f7f4ed"
WHITE = "#fffdf8"
CHARCOAL = "#26302b"
MOSS = "#475f4c"
CEDAR = "#8a603d"
LINE = "#d7ddd3"
PALE = "#eee7da"


def f(path, size):
    return ImageFont.truetype(str(path), size=size)


def cover(path, size, centering=(0.5, 0.5)):
    img = Image.open(path).convert("RGB")
    img = ImageOps.exif_transpose(img)
    return ImageOps.fit(img, size, method=Image.Resampling.LANCZOS, centering=centering)


def wrap(draw, text, font, width):
    lines = []
    current = ""
    for char in text:
        candidate = current + char
        if draw.textlength(candidate, font=font) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = char
    if current:
        lines.append(current)
    return lines


def text_block(draw, xy, text, font, fill, width, gap=10):
    x, y = xy
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + gap
    return y


def rounded(draw, xy, r=18, fill=WHITE, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def button(draw, xy, text, fill=CHARCOAL, color=WHITE, w=220):
    x, y = xy
    rounded(draw, (x, y, x + w, y + 58), 8, fill=fill)
    font = f(FONT_SANS, 24)
    tw = draw.textlength(text, font=font)
    draw.text((x + (w - tw) / 2, y + 14), text, font=font, fill=color)


def chip(draw, xy, text, fill=PALE, color=INK):
    x, y = xy
    font = f(FONT_SANS, 19)
    w = int(draw.textlength(text, font=font) + 34)
    rounded(draw, (x, y, x + w, y + 38), 18, fill=fill)
    draw.text((x + 17, y + 6), text, font=font, fill=color)
    return x + w + 10


def header(draw, w, active="TOP"):
    draw.rectangle((0, 0, w, 84), fill=PAPER)
    draw.line((0, 84, w, 84), fill=LINE, width=2)
    draw.ellipse((70, 24, 118, 72), fill=CHARCOAL)
    draw.text((87, 31), "余", font=f(FONT_SERIF, 24), fill=WHITE)
    draw.text((136, 29), "YOHAKU", font=f(FONT_SANS, 30), fill=INK)
    nav = ["TOP", "商品", "ギフト", "受注生産", "FAQ"]
    x = 650
    for item in nav:
        color = CEDAR if item == active else MUTED
        draw.text((x, 34), item, font=f(FONT_SANS, 20), fill=color)
        x += 100
    button(draw, (1180, 18), "予約する", w=150)


def page_frame(title):
    W, H = 1440, 1900
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    header(draw, W, title)
    return img, draw


def create_structure():
    W, H = 1800, 1200
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw.text((80, 70), "YOHAKU Online Order Site Structure", font=f(FONT_SANS, 34), fill=CEDAR)
    draw.text((80, 125), "受注生産で予約を受け、用途別に選びやすくするページ階層", font=f(FONT_SERIF, 54), fill=INK)

    nodes = [
        ("TOP LP", "世界観・用途・受注生産の安心感", (760, 250), MOSS),
        ("商品詳細", "朝のお堂 / 親孝香 / 凛香 / 築地、午前六時", (160, 500), WHITE),
        ("用途別ギフト", "両親 / 飲食店 / 美容サロン / クリニック / 富裕層寝室", (630, 500), WHITE),
        ("受注生産フォーム", "香り・本数・包装・配送希望・連絡先", (1100, 500), WHITE),
        ("法人/店舗相談", "10本以上・VIPギフト・オリジナルカード", (430, 770), WHITE),
        ("FAQ/安心表示", "納期・香りの強さ・返品・医師監修表現", (890, 770), WHITE),
        ("Thanks", "受付完了・納期案内・LINE/メール誘導", (1350, 770), WHITE),
    ]

    def box(label, desc, pos, fill):
        x, y = pos
        rounded(draw, (x, y, x + 360, y + 145), 20, fill=fill, outline=LINE, width=2)
        text_color = WHITE if fill == MOSS else INK
        muted = "#e4eadf" if fill == MOSS else MUTED
        draw.text((x + 28, y + 28), label, font=f(FONT_SANS, 31), fill=text_color)
        text_block(draw, (x + 28, y + 76), desc, f(FONT_SANS, 20), muted, 300, gap=8)

    for label, desc, pos, fill in nodes:
        box(label, desc, pos, fill)

    lines = [
        ((940, 395), (340, 500)),
        ((940, 395), (810, 500)),
        ((940, 395), (1280, 500)),
        ((810, 645), (610, 770)),
        ((810, 645), (1070, 770)),
        ((1280, 645), (1530, 770)),
    ]
    for a, b in lines:
        draw.line((a[0], a[1], b[0], b[1]), fill=CEDAR, width=4)
        draw.ellipse((b[0] - 5, b[1] - 5, b[0] + 5, b[1] + 5), fill=CEDAR)

    rounded(draw, (80, 1000, 1720, 1120), 22, fill=WHITE, outline=LINE, width=2)
    draw.text((120, 1034), "購入導線", font=f(FONT_SANS, 28), fill=INK)
    draw.text(
        (280, 1038),
        "TOPで世界観を理解 → 用途または香りから選ぶ → 受注生産フォーム → 受付完了メール → 製造/発送",
        font=f(FONT_SANS, 25),
        fill=MUTED,
    )
    img.save(OUT / "lp-00-site-structure.png", quality=95)


def create_top_page():
    img, draw = page_frame("TOP")
    hero = cover(ASSETS / "yohaku-hero.png", (680, 620), (0.58, 0.5))
    img.paste(hero, (690, 132))
    overlay = Image.new("RGBA", (680, 620), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((0, 0, 230, 620), fill=(247, 244, 237, 225))
    img.paste(overlay, (690, 132), overlay)

    draw.text((70, 170), "TSUKIJI TEMPLE FRAGRANCE", font=f(FONT_SANS, 22), fill=CEDAR)
    draw.text((70, 220), "和の静けさを、\n部屋の余白に。", font=f(FONT_SERIF, 82), fill=INK, spacing=12)
    text_block(draw, (70, 455), "築地・法重寺の朝のお堂から着想した、受注生産のルームディフューザー。落ち着いた静寂を好む両親へ、和の飲食店や美容サロンの上顧客へ、富裕層の寝室へ。", f(FONT_SANS, 27), MUTED, 560, gap=13)
    button(draw, (70, 650), "香りを選んで予約", w=280)
    button(draw, (370, 650), "ギフト用途を見る", fill=WHITE, color=INK, w=240)

    y = 845
    draw.text((70, y), "用途から選ぶ", font=f(FONT_SERIF, 54), fill=INK)
    cards = [
        ("親孝香", "両親へ贈る静かな親孝行", ASSETS / "concepts" / "parents-gift.png"),
        ("凛香", "和の店舗・美容サロンのVIPギフト", ASSETS / "concepts" / "vip-hospitality.png"),
        ("築地、午前六時", "都心の寝室に戻る静寂", ASSETS / "concepts" / "luxury-bedroom.png"),
    ]
    x = 70
    for title, desc, p in cards:
        rounded(draw, (x, y + 95, x + 400, y + 520), 18, fill=WHITE, outline=LINE, width=2)
        img.paste(cover(p, (400, 250)), (x, y + 95))
        draw.text((x + 26, y + 375), title, font=f(FONT_SERIF, 37), fill=INK)
        draw.text((x + 26, y + 432), desc, font=f(FONT_SANS, 22), fill=MUTED)
        x += 440

    y = 1470
    rounded(draw, (70, y, 1370, y + 240), 24, fill=CHARCOAL)
    draw.text((120, y + 52), "受注生産だから、無駄なく、丁寧に。", font=f(FONT_SERIF, 45), fill=WHITE)
    text_block(draw, (120, y + 120), "予約受付後に製造数を確定。初回は限定108本から開始し、ギフト包装・法人注文・オリジナルカードにも対応します。", f(FONT_SANS, 25), "#d8cdbb", 900, gap=10)
    button(draw, (1080, y + 92), "予約フォームへ", fill=WHITE, color=INK, w=230)
    img.save(OUT / "lp-01-top.png", quality=95)


def create_product_page():
    img, draw = page_frame("商品")
    product = cover(ASSETS / "yohaku-hero.png", (560, 560), (0.62, 0.5))
    img.paste(product, (70, 150))
    draw.text((700, 160), "First Collection", font=f(FONT_SANS, 24), fill=CEDAR)
    draw.text((700, 215), "朝のお堂", font=f(FONT_SERIF, 72), fill=INK)
    draw.text((700, 305), "100ml / 約8週間 / 9,900円 税込", font=f(FONT_SANS, 27), fill=INK)
    text_block(draw, (700, 370), "檜、白檀、柚子、茶の奥行き。強く主張しすぎず、玄関、寝室、書斎の印象を静かに整える一本です。", f(FONT_SANS, 27), MUTED, 560, gap=12)
    x = 700
    for item in ["檜", "白檀", "柚子", "茶", "受注生産"]:
        x = chip(draw, (x, 545), item, PALE, INK)
    button(draw, (700, 625), "この香りで予約", w=250)

    y = 810
    draw.text((70, y), "予約フォーム イメージ", font=f(FONT_SERIF, 52), fill=INK)
    rounded(draw, (70, y + 90, 1370, y + 720), 24, fill=WHITE, outline=LINE, width=2)
    fields = [
        ("香り", "朝のお堂"),
        ("本数", "1本 / 3本 / 10本以上"),
        ("用途", "自宅用 / 両親ギフト / 店舗ギフト / 法人ギフト"),
        ("包装", "通常 / ギフト包装 / メッセージカード"),
        ("お届け希望", "2026年8月上旬以降"),
    ]
    fx, fy = 120, y + 150
    for label, value in fields:
        draw.text((fx, fy), label, font=f(FONT_SANS, 22), fill=CEDAR)
        rounded(draw, (fx, fy + 38, fx + 560, fy + 94), 8, fill=PAPER, outline=LINE, width=2)
        draw.text((fx + 22, fy + 52), value, font=f(FONT_SANS, 24), fill=INK)
        fy += 112
        if fy > y + 560:
            fx = 740
            fy = y + 150
    rounded(draw, (740, y + 150, 1320, y + 520), 18, fill=PALE)
    draw.text((780, y + 195), "受注生産の流れ", font=f(FONT_SANS, 32), fill=INK)
    steps = ["1. 予約受付", "2. 製造数確定", "3. 調香・充填・包装", "4. 発送連絡"]
    sy = y + 260
    for step in steps:
        draw.text((780, sy), step, font=f(FONT_SANS, 26), fill=MUTED)
        sy += 58
    button(draw, (1040, y + 590), "予約内容を確認", w=250)
    img.save(OUT / "lp-02-product-order.png", quality=95)


def create_gift_page():
    img, draw = page_frame("ギフト")
    draw.text((70, 145), "Gift & Business", font=f(FONT_SANS, 24), fill=CEDAR)
    draw.text((70, 200), "贈る相手の暮らしに、\n静けさを届ける。", font=f(FONT_SERIF, 68), fill=INK, spacing=10)
    text_block(draw, (760, 210), "両親への節目の贈り物、和の飲食店の手土産、美容サロンやクリニックのVIPギフト、不動産成約祝いまで。用途に合わせて香り・包装・カードを選べます。", f(FONT_SANS, 27), MUTED, 560, gap=13)

    cards = [
        ("両親ギフト", "親孝香", "母の日・父の日・敬老の日へ", ASSETS / "concepts" / "parents-gift.png"),
        ("店舗/サロンVIP", "凛香", "上顧客の記憶に残る手土産", ASSETS / "concepts" / "vip-hospitality.png"),
        ("富裕層寝室", "築地、午前六時", "移転祝い・成約祝いにも", ASSETS / "concepts" / "luxury-bedroom.png"),
    ]
    y = 560
    for i, (label, title, desc, p) in enumerate(cards):
        x = 70 + i * 440
        rounded(draw, (x, y, x + 400, y + 540), 18, fill=WHITE, outline=LINE, width=2)
        img.paste(cover(p, (400, 270)), (x, y))
        draw.text((x + 26, y + 310), label, font=f(FONT_SANS, 23), fill=CEDAR)
        draw.text((x + 26, y + 355), title, font=f(FONT_SERIF, 38), fill=INK)
        text_block(draw, (x + 26, y + 415), desc, f(FONT_SANS, 22), MUTED, 330, gap=8)
        button(draw, (x + 26, y + 470), "この用途で相談", fill=CHARCOAL, color=WHITE, w=210)

    y = 1240
    rounded(draw, (70, y, 1370, y + 420), 26, fill=CHARCOAL)
    draw.text((120, y + 60), "法人・店舗向け注文", font=f(FONT_SERIF, 54), fill=WHITE)
    text_block(draw, (120, y + 145), "10本以上のギフト注文、熨斗、メッセージカード、店舗名入りカード、納期相談に対応。まずは用途と本数を入力して相談できます。", f(FONT_SANS, 27), "#d8cdbb", 780, gap=12)
    rounded(draw, (980, y + 82, 1305, y + 315), 18, fill=WHITE)
    draw.text((1025, y + 125), "相談フォーム", font=f(FONT_SANS, 30), fill=INK)
    draw.text((1025, y + 185), "用途 / 本数 / 希望納期", font=f(FONT_SANS, 23), fill=MUTED)
    button(draw, (1025, y + 240), "法人相談へ", fill=MOSS, color=WHITE, w=210)
    img.save(OUT / "lp-03-gift-business.png", quality=95)


def main():
    create_structure()
    create_top_page()
    create_product_page()
    create_gift_page()


if __name__ == "__main__":
    main()
