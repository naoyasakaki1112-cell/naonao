from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageOps
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUT = ROOT / "output" / "pdf"
TMP = ROOT / "tmp" / "pdfs"
OUT.mkdir(parents=True, exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)

PDF_PATH = OUT / "yohaku-a4-flyer.pdf"
PNG_PATH = OUT / "yohaku-a4-flyer.png"
HERO = ASSETS / "yohaku-hero.png"
DOCTOR = ASSETS / "doctor-supervisor.png"

FONT_SANS = r"C:\Windows\Fonts\NotoSansJP-VF.ttf"
FONT_SERIF = r"C:\Windows\Fonts\NotoSerifJP-VF.ttf"
pdfmetrics.registerFont(TTFont("NotoSansJP", FONT_SANS))
pdfmetrics.registerFont(TTFont("NotoSerifJP", FONT_SERIF))

W, H = A4


def hex_color(value):
    value = value.lstrip("#")
    return colors.HexColor("#" + value)


INK = hex_color("18211e")
MUTED = hex_color("66726b")
PAPER = hex_color("f7f4ed")
PAPER_DEEP = hex_color("ebe5d8")
MOSS = hex_color("475f4c")
CEDAR = hex_color("8a603d")
CHARCOAL = hex_color("26302b")
WHITE = hex_color("fffdf8")
LINE = hex_color("d7ddd3")


def cover_crop(src, dst, size):
    img = Image.open(src).convert("RGB")
    img = ImageOps.exif_transpose(img)
    target_w, target_h = size
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    new_size = (int(src_w * scale), int(src_h * scale))
    img = img.resize(new_size, Image.Resampling.LANCZOS)
    left = (img.width - target_w) // 2
    top = (img.height - target_h) // 2
    img = img.crop((left, top, left + target_w, top + target_h))
    img.save(dst, quality=95)


def circle_crop(src, dst, size):
    img = Image.open(src).convert("RGB")
    img = ImageOps.exif_transpose(img)
    img = ImageOps.fit(img, (size, size), method=Image.Resampling.LANCZOS, centering=(0.5, 0.34))
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size - 1, size - 1), fill=255)
    out = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    out.paste(img, (0, 0), mask)
    out.save(dst)


def draw_wrapped(c, text, x, y, max_width, font_name, font_size, leading, color=INK):
    c.setFillColor(color)
    c.setFont(font_name, font_size)
    lines = []
    current = ""
    for char in text:
        candidate = current + char
        if pdfmetrics.stringWidth(candidate, font_name, font_size) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = char
    if current:
        lines.append(current)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_label(c, text, x, y, w, h, fill, text_color=WHITE):
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, 3, stroke=0, fill=1)
    c.setFillColor(text_color)
    c.setFont("NotoSansJP", 8.5)
    c.drawCentredString(x + w / 2, y + 7.8, text)


def build_pdf():
    hero_crop = TMP / "flyer-hero-crop.jpg"
    doctor_crop = TMP / "doctor-circle.png"
    cover_crop(HERO, hero_crop, (1500, 1050))
    circle_crop(DOCTOR, doctor_crop, 420)

    c = canvas.Canvas(str(PDF_PATH), pagesize=A4)
    c.setTitle("YOHAKU A4 Flyer")

    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    margin = 34
    top_y = H - 34

    c.setFillColor(CHARCOAL)
    c.circle(margin + 12, top_y - 8, 12, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("NotoSerifJP", 11)
    c.drawCentredString(margin + 12, top_y - 12, "余")
    c.setFillColor(INK)
    c.setFont("NotoSansJP", 15)
    c.drawString(margin + 32, top_y - 14, "YOHAKU")
    c.setFont("NotoSansJP", 8.5)
    c.setFillColor(CEDAR)
    c.drawRightString(W - margin, top_y - 10, "TSUKIJI TEMPLE FRAGRANCE")

    hero_x, hero_y, hero_w, hero_h = margin, 432, W - margin * 2, 302
    c.drawImage(str(hero_crop), hero_x, hero_y, hero_w, hero_h, preserveAspectRatio=False, mask="auto")
    c.setFillColor(colors.Color(0, 0, 0, alpha=0.32))
    c.rect(hero_x, hero_y, hero_w * 0.52, hero_h, stroke=0, fill=1)

    c.setFillColor(WHITE)
    c.setFont("NotoSansJP", 8.5)
    c.drawString(hero_x + 24, hero_y + hero_h - 45, "限定108本 予約販売")
    c.setFont("NotoSerifJP", 34)
    c.drawString(hero_x + 24, hero_y + hero_h - 88, "和の静けさを、")
    c.drawString(hero_x + 24, hero_y + hero_h - 130, "部屋の余白に。")
    c.setFont("NotoSansJP", 11)
    lead = "築地・法重寺の朝のお堂から着想した、寺ブランドのルームディフューザー。檜、白檀、柚子、茶の奥行きで、ホテルライクな空間に日本らしい凛とした空気を重ねます。"
    draw_wrapped(c, lead, hero_x + 24, hero_y + 128, 250, "NotoSansJP", 10.5, 17, WHITE)
    draw_label(c, "100ml", hero_x + 24, hero_y + 26, 52, 22, CEDAR)
    draw_label(c, "約8週間", hero_x + 84, hero_y + 26, 62, 22, CEDAR)
    draw_label(c, "9,900円", hero_x + 154, hero_y + 26, 70, 22, CEDAR)

    c.setFillColor(INK)
    c.setFont("NotoSerifJP", 21)
    c.drawString(margin, 390, "朝のお堂")
    c.setFont("NotoSansJP", 9)
    c.setFillColor(CEDAR)
    c.drawString(margin, 372, "Hinoki / Sandalwood / Yuzu / Japanese Tea")
    body = "清潔感のある檜に、白檀の深さ、柚子の明るさ、茶の落ち着きを重ねた一本。強く主張せず、玄関、寝室、書斎の印象を静かに整えます。"
    draw_wrapped(c, body, margin, 348, 245, "NotoSansJP", 10.5, 17, MUTED)

    spec_x = 332
    c.setFillColor(WHITE)
    c.roundRect(spec_x, 334, 228, 64, 8, stroke=0, fill=1)
    c.setStrokeColor(LINE)
    c.roundRect(spec_x, 334, 228, 64, 8, stroke=1, fill=0)
    c.setFont("NotoSansJP", 8.5)
    c.setFillColor(MUTED)
    c.drawString(spec_x + 18, 377, "FIRST COLLECTION")
    c.setFillColor(INK)
    c.setFont("NotoSansJP", 14)
    c.drawString(spec_x + 18, 354, "予約価格 9,900円 税込")
    c.setFont("NotoSansJP", 9)
    c.setFillColor(MUTED)
    c.drawString(spec_x + 18, 340, "初回発送予定: 2026年8月上旬")

    feature_y = 232
    features = [
        ("01", "洋の高級感", "ホテルライクな清潔感を持ちながら、和の素材感で差別化。"),
        ("02", "寺の物語", "ご利益ではなく、法重寺の静けさを空間体験として表現。"),
        ("03", "贈れる佇まい", "墨色ボトルと和紙ラベルで、法人ギフトにも対応。"),
    ]
    card_w = (W - margin * 2 - 16) / 3
    for i, (num, title, desc) in enumerate(features):
        x = margin + i * (card_w + 8)
        c.setFillColor(WHITE)
        c.roundRect(x, feature_y, card_w, 78, 6, stroke=0, fill=1)
        c.setStrokeColor(LINE)
        c.roundRect(x, feature_y, card_w, 78, 6, stroke=1, fill=0)
        c.setFont("NotoSansJP", 8.5)
        c.setFillColor(CEDAR)
        c.drawString(x + 12, feature_y + 56, num)
        c.setFont("NotoSansJP", 12)
        c.setFillColor(INK)
        c.drawString(x + 12, feature_y + 38, title)
        draw_wrapped(c, desc, x + 12, feature_y + 21, card_w - 24, "NotoSansJP", 8.0, 10.5, MUTED)

    c.setFillColor(CHARCOAL)
    c.roundRect(margin, 98, W - margin * 2, 112, 8, stroke=0, fill=1)
    c.drawImage(str(doctor_crop), margin + 18, 119, 70, 70, mask="auto")
    c.setFillColor(WHITE)
    c.setFont("NotoSansJP", 10)
    c.drawString(margin + 104, 183, "医師監修コメント")
    c.setFont("NotoSansJP", 8.3)
    c.setFillColor(hex_color("d8cdbb"))
    c.drawString(margin + 104, 168, "消化器内科医 岡原医師")
    comment = "香りは治療を目的とするものではありませんが、帰宅後の環境を整えるきっかけになります。YOHAKUは強く主張しすぎない香調で、日々の休息時間に取り入れやすい設計だと感じます。"
    draw_wrapped(c, comment, margin + 104, 149, 390, "NotoSansJP", 8.6, 13, WHITE)
    c.setFillColor(hex_color("bfc7bd"))
    c.setFont("NotoSansJP", 6.8)
    c.drawRightString(W - margin - 14, 108, "※医師画像はAI生成によるイメージです。医療効果を示すものではありません。")

    c.setFillColor(WHITE)
    c.roundRect(margin, 30, W - margin * 2, 50, 6, stroke=0, fill=1)
    c.setStrokeColor(LINE)
    c.roundRect(margin, 30, W - margin * 2, 50, 6, stroke=1, fill=0)
    c.setFillColor(INK)
    c.setFont("NotoSansJP", 11)
    c.drawString(margin + 18, 58, "限定108本 予約受付中")
    c.setFont("NotoSansJP", 8.5)
    c.setFillColor(MUTED)
    c.drawString(margin + 18, 43, "自宅用、移転祝い、上顧客向けギフト、法人ノベルティのご相談も承ります。")
    c.setFillColor(CHARCOAL)
    c.roundRect(W - margin - 132, 41, 112, 28, 4, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("NotoSansJP", 10)
    c.drawCentredString(W - margin - 76, 50, "予約サイトへ")

    c.save()


def main():
    build_pdf()
    print(PDF_PATH)


if __name__ == "__main__":
    main()
