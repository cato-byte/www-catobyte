"""Generate the 1200x630 social preview images (Open Graph) used by the site.

LinkedIn and most chat apps don't render SVG previews, so these are PNGs.
Run from the repo root:  python scripts/make_share_images.py
"""

from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = Path("/usr/share/fonts/truetype/noto")
W, H = 1200, 630

NAVY = (11, 17, 32)
PANEL = (20, 30, 51)
TEXT = (230, 235, 245)
MUTED = (154, 168, 191)
ACCENT = (126, 162, 255)
LAYERS = [
    ("Landing", (100, 116, 139)),
    ("Bronze", (176, 106, 43)),
    ("Staging", (71, 85, 105)),
    ("Vault", (37, 84, 217)),
    ("Gold", (202, 150, 18)),
]


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / f"NotoSans-{weight}.ttf"), size)


def centered(draw, box, text, fnt, fill):
    x0, y0, x1, y1 = box
    draw.text(((x0 + x1) / 2, (y0 + y1) / 2), text, font=fnt, fill=fill, anchor="mm")


def default_image(path: Path, owner: dict) -> None:
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    d.rectangle((0, H - 10, W, H), fill=ACCENT)
    d.rounded_rectangle((80, 90, 180, 190), radius=22, fill=ACCENT)
    centered(d, (80, 90, 180, 190), owner["initials"], font("Bold", 64), NAVY)
    d.text((80, 240), owner["name"], font=font("Bold", 92), fill=TEXT)
    d.text((80, 360), "Data Engineer", font=font("SemiBold", 52), fill=ACCENT)
    d.text((80, 440), "Spark · Databricks · AWS · Data Vault", font=font("Regular", 34), fill=MUTED)
    d.text((80, 535), "catobyte.co", font=font("SemiBold", 30), fill=TEXT)
    if owner.get("photo"):
        size = 340
        photo = Image.open(ROOT / owner["photo"]).convert("RGB").resize((size, size), Image.LANCZOS)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
        d.ellipse((780 - 6, 140 - 6, 780 + size + 6, 140 + size + 6), fill=ACCENT)
        img.paste(photo, (780, 140), mask)
    img.save(path, optimize=True)


def project_cover(path: Path) -> None:
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    d.text((60, 52), "Pan-European Company Registry Lakehouse", font=font("Bold", 48), fill=TEXT)
    d.text((60, 125), "6 national registers · Data Vault 2.0 · Databricks on AWS", font=font("Regular", 30), fill=MUTED)

    # Country chips, 2 columns x 3 rows.
    chip_font = font("Bold", 30)
    countries = ["FR", "IE", "UK", "NO", "EE", "ES"]
    top = 250
    for i, code in enumerate(countries):
        col, row = i % 2, i // 2
        x, y = 60 + col * 110, top + row * 100
        d.rounded_rectangle((x, y, x + 92, y + 72), radius=14, fill=PANEL, outline=ACCENT, width=2)
        centered(d, (x, y, x + 92, y + 72), code, chip_font, TEXT)

    # Arrow from the chips into the layers.
    d.line((290, 380, 330, 380), fill=MUTED, width=4)
    d.polygon([(330, 370), (346, 380), (330, 390)], fill=MUTED)

    # Medallion / vault layers.
    layer_font = font("SemiBold", 26)
    x, box_w, gap = 362, 136, 18
    for i, (name, colour) in enumerate(LAYERS):
        x0 = x + i * (box_w + gap)
        d.rounded_rectangle((x0, 300, x0 + box_w, 460), radius=16, fill=colour)
        centered(d, (x0, 300, x0 + box_w, 460), name, layer_font, (255, 255, 255))
        if i < len(LAYERS) - 1:
            ax = x0 + box_w + 3
            d.polygon([(ax, 370), (ax + 13, 380), (ax, 390)], fill=MUTED)

    d.text((362, 500), "Lambda  ›  S3  ›  Delta Lake  ›  Hubs, Links, Satellites  ›  dim & fact",
           font=font("Regular", 24), fill=MUTED)
    d.rectangle((0, H - 10, W, H), fill=ACCENT)
    img.save(path, optimize=True)


if __name__ == "__main__":
    site = yaml.safe_load((ROOT / "site.yaml").read_text(encoding="utf-8"))
    default_image(ROOT / "images" / "og-default.png", site["owner"])
    project_cover(ROOT / "images" / "projects" / "eu-company-registry.png")
    print("Share images written to images/")
