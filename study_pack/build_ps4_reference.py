from __future__ import annotations

import math
import os
from io import BytesIO
from pathlib import Path
from typing import Iterable, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image as PILImage
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

# -----------------------------------------------------------------------------
# Paths and fonts
# -----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
ASSET = OUT / "assets"
OUT.mkdir(parents=True, exist_ok=True)
ASSET.mkdir(parents=True, exist_ok=True)
PDF_PATH = OUT / "finance_lectures_1_7_final_ps4_reference.pdf"

FONT_CANDIDATES = [
    Path("/usr/share/fonts/truetype/nanum/NanumGothic.ttf"),
    Path("/usr/share/fonts/truetype/nanum/NanumGothicCoding.ttf"),
]
BOLD_CANDIDATES = [
    Path("/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"),
    Path("/usr/share/fonts/truetype/nanum/NanumGothicCoding-Bold.ttf"),
]
FONT_REG = next((p for p in FONT_CANDIDATES if p.exists()), None)
FONT_BOLD = next((p for p in BOLD_CANDIDATES if p.exists()), None)
if FONT_REG is None or FONT_BOLD is None:
    raise FileNotFoundError("NanumGothic fonts were not found. Install fonts-nanum.")

pdfmetrics.registerFont(TTFont("NanumGothic", str(FONT_REG)))
pdfmetrics.registerFont(TTFont("NanumGothicBold", str(FONT_BOLD)))

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["mathtext.fontset"] = "dejavusans"
plt.rcParams["axes.unicode_minus"] = False

# -----------------------------------------------------------------------------
# Theme
# -----------------------------------------------------------------------------
NAVY = HexColor("#17365D")
BLUE = HexColor("#2F5597")
TEAL = HexColor("#0F6B78")
GREEN = HexColor("#2E7D5A")
ORANGE = HexColor("#C45A19")
RED = HexColor("#A52A2A")
INK = HexColor("#20252B")
MID = HexColor("#5C6670")
PALE_BLUE = HexColor("#EAF1F8")
PALE_TEAL = HexColor("#E8F4F4")
PALE_GREEN = HexColor("#EAF5EF")
PALE_ORANGE = HexColor("#FFF1E6")
PALE_RED = HexColor("#FBEAEA")
LIGHT = HexColor("#F5F7F9")
LINE = HexColor("#D6DCE2")
WHITE = colors.white

PAGE_W, PAGE_H = A4
LEFT = 17 * mm
RIGHT = 17 * mm
TOP = 18 * mm
BOTTOM = 17 * mm
CONTENT_W = PAGE_W - LEFT - RIGHT

# -----------------------------------------------------------------------------
# Styles
# -----------------------------------------------------------------------------
styles = getSampleStyleSheet()
BODY = ParagraphStyle(
    "BodyKR",
    parent=styles["BodyText"],
    fontName="NanumGothic",
    fontSize=9.3,
    leading=14.1,
    textColor=INK,
    alignment=TA_LEFT,
    wordWrap="CJK",
    spaceAfter=4,
)
BODY_SMALL = ParagraphStyle(
    "BodySmallKR",
    parent=BODY,
    fontSize=8.2,
    leading=12.3,
    textColor=MID,
)
BODY_TINY = ParagraphStyle(
    "BodyTinyKR",
    parent=BODY,
    fontSize=7.4,
    leading=10.4,
)
H1 = ParagraphStyle(
    "H1KR",
    parent=styles["Heading1"],
    fontName="NanumGothicBold",
    fontSize=20,
    leading=26,
    textColor=NAVY,
    wordWrap="CJK",
    spaceBefore=2,
    spaceAfter=9,
)
H2 = ParagraphStyle(
    "H2KR",
    parent=styles["Heading2"],
    fontName="NanumGothicBold",
    fontSize=14.5,
    leading=20,
    textColor=NAVY,
    wordWrap="CJK",
    spaceBefore=8,
    spaceAfter=6,
)
H3 = ParagraphStyle(
    "H3KR",
    parent=styles["Heading3"],
    fontName="NanumGothicBold",
    fontSize=11.2,
    leading=15,
    textColor=TEAL,
    wordWrap="CJK",
    spaceBefore=5,
    spaceAfter=4,
)
TITLE = ParagraphStyle(
    "TitleKR",
    parent=styles["Title"],
    fontName="NanumGothicBold",
    fontSize=27,
    leading=35,
    textColor=WHITE,
    alignment=TA_LEFT,
    wordWrap="CJK",
)
SUBTITLE = ParagraphStyle(
    "SubtitleKR",
    parent=BODY,
    fontName="NanumGothic",
    fontSize=12.5,
    leading=19,
    textColor=WHITE,
)
CENTER = ParagraphStyle(
    "CenterKR",
    parent=BODY,
    alignment=TA_CENTER,
)
BOX_TITLE = ParagraphStyle(
    "BoxTitleKR",
    parent=BODY,
    fontName="NanumGothicBold",
    fontSize=10.2,
    leading=14.5,
    textColor=NAVY,
    spaceAfter=3,
)
TABLE_HEAD = ParagraphStyle(
    "TableHeadKR",
    parent=BODY,
    fontName="NanumGothicBold",
    fontSize=8.2,
    leading=11.5,
    textColor=WHITE,
    alignment=TA_CENTER,
)
TABLE_BODY = ParagraphStyle(
    "TableBodyKR",
    parent=BODY,
    fontSize=7.8,
    leading=11.2,
    spaceAfter=0,
)
TABLE_BODY_CENTER = ParagraphStyle(
    "TableBodyCenterKR",
    parent=TABLE_BODY,
    alignment=TA_CENTER,
)
QUOTE = ParagraphStyle(
    "QuoteKR",
    parent=BODY,
    fontName="NanumGothicBold",
    fontSize=10.5,
    leading=16,
    textColor=BLUE,
    leftIndent=8,
    rightIndent=8,
    alignment=TA_CENTER,
)

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def P(text: str, style: ParagraphStyle = BODY) -> Paragraph:
    return Paragraph(text, style)


def bullet(text: str, level: int = 0, strong: bool = False) -> Paragraph:
    style = ParagraphStyle(
        f"Bullet{level}{strong}",
        parent=BODY,
        fontName="NanumGothicBold" if strong else "NanumGothic",
        leftIndent=12 + level * 12,
        firstLineIndent=-9,
        bulletIndent=0,
        spaceAfter=2.5,
    )
    return Paragraph(f"• {text}", style)


def label(text: str, bg: colors.Color = NAVY) -> Table:
    t = Table([[P(text, ParagraphStyle("Label", parent=BODY, fontName="NanumGothicBold", fontSize=8.2, leading=10, textColor=WHITE, alignment=TA_CENTER))]], colWidths=[42 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0, bg),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def callout(title: str, body: str, bg: colors.Color = PALE_BLUE, bar: colors.Color = BLUE) -> Table:
    cell = [P(title, BOX_TITLE), P(body, BODY)]
    t = Table([["", cell]], colWidths=[3.2 * mm, CONTENT_W - 3.2 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), bar),
        ("BACKGROUND", (1, 0), (1, 0), bg),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("RIGHTPADDING", (0, 0), (0, 0), 0),
        ("TOPPADDING", (0, 0), (0, 0), 0),
        ("BOTTOMPADDING", (0, 0), (0, 0), 0),
        ("LEFTPADDING", (1, 0), (1, 0), 9),
        ("RIGHTPADDING", (1, 0), (1, 0), 9),
        ("TOPPADDING", (1, 0), (1, 0), 8),
        ("BOTTOMPADDING", (1, 0), (1, 0), 8),
        ("BOX", (0, 0), (-1, -1), 0.6, LINE),
    ]))
    return t


def section_title(kicker: str, title: str, desc: str = "") -> List:
    out: List = [Spacer(1, 2), label(kicker), Spacer(1, 7), P(title, H1)]
    if desc:
        out.append(P(desc, BODY_SMALL))
    out.append(Spacer(1, 3))
    return out


def equation(tex: str, width: float = 145 * mm, fontsize: int = 18, pad: float = 0.12) -> Image:
    fig = plt.figure(figsize=(8.4, 0.65), dpi=240)
    fig.patch.set_alpha(0)
    fig.text(0.5, 0.5, f"${tex}$", ha="center", va="center", fontsize=fontsize)
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=240, transparent=True, bbox_inches="tight", pad_inches=pad)
    plt.close(fig)
    buf.seek(0)
    img = Image(buf)
    ratio = img.imageHeight / img.imageWidth
    img.drawWidth = width
    img.drawHeight = width * ratio
    img.hAlign = "CENTER"
    return img


def formula_card(title: str, tex: str, note: str = "", bg: colors.Color = LIGHT, width: float = CONTENT_W) -> Table:
    parts: List = [P(title, BOX_TITLE), equation(tex, width=min(140 * mm, width - 20 * mm), fontsize=17)]
    if note:
        parts.append(P(note, BODY_SMALL))
    t = Table([[parts]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.7, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def two_col(left: Iterable, right: Iterable, left_w: float = 0.5, gap: float = 6 * mm) -> Table:
    lw = CONTENT_W * left_w - gap / 2
    rw = CONTENT_W - lw - gap
    t = Table([[list(left), list(right)]], colWidths=[lw, rw], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("RIGHTPADDING", (0, 0), (0, 0), gap / 2),
        ("LEFTPADDING", (1, 0), (1, 0), gap / 2),
        ("RIGHTPADDING", (1, 0), (1, 0), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def data_table(headers: List[str], rows: List[List[str]], widths: List[float], font_size: float = 7.8) -> Table:
    hs = [P(h, TABLE_HEAD) for h in headers]
    body_style = ParagraphStyle("TableCustom", parent=TABLE_BODY, fontSize=font_size, leading=font_size * 1.42)
    data = [hs] + [[P(str(c), body_style) for c in row] for row in rows]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def add_image(path: Path, width: float = CONTENT_W, max_h: float = 105 * mm) -> Image:
    img = Image(str(path))
    ratio = img.imageHeight / img.imageWidth
    h = width * ratio
    if h > max_h:
        h = max_h
        width = h / ratio
    img.drawWidth = width
    img.drawHeight = h
    img.hAlign = "CENTER"
    return img

# -----------------------------------------------------------------------------
# Charts
# -----------------------------------------------------------------------------
def save_generic_frontier(path: Path) -> None:
    w = np.linspace(0, 1, 501)
    mu_a, mu_b = 1.0, 2.0
    s_a, s_b = 0.75, 1.35
    plt.figure(figsize=(7.5, 4.4))
    for rho, ls in [(1.0, "-"), (0.0, "--"), (-1.0, ":")]:
        mu = w * mu_a + (1 - w) * mu_b
        var = w**2 * s_a**2 + (1 - w)**2 * s_b**2 + 2 * w * (1 - w) * rho * s_a * s_b
        sig = np.sqrt(np.maximum(var, 0))
        plt.plot(sig, mu, linestyle=ls, linewidth=2.2, label=rf"$\rho_{{AB}}={rho:g}$")
    plt.scatter([s_a, s_b], [mu_a, mu_b], s=45)
    plt.annotate("A", (s_a, mu_a), xytext=(6, -12), textcoords="offset points")
    plt.annotate("B", (s_b, mu_b), xytext=(6, 5), textcoords="offset points")
    plt.xlabel(r"Risk  $\sigma_p$")
    plt.ylabel(r"Expected return  $\bar r_p$")
    plt.title("Correlation determines the shape of the two-asset frontier")
    plt.grid(alpha=0.2)
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(path, dpi=220, bbox_inches="tight")
    plt.close()


def save_ex1_frontier(path: Path) -> None:
    s_m = 1 / math.sqrt(2)
    s_a = math.sqrt(2 / 3)
    s_b = math.sqrt(2)
    plt.figure(figsize=(7.5, 4.1))
    x = np.linspace(s_m, s_b, 100)
    plt.plot(x, np.full_like(x, 2.0), linewidth=3)
    plt.scatter([s_m, s_a, s_b], [2, 2, 2], s=[70, 55, 55])
    plt.annotate(r"MVP / T  $(1/\sqrt{2},2)$", (s_m, 2), xytext=(-15, 28), textcoords="offset points")
    plt.annotate(r"A  $(\sqrt{2/3},2)$", (s_a, 2), xytext=(5, -25), textcoords="offset points")
    plt.annotate(r"B  $(\sqrt{2},2)$", (s_b, 2), xytext=(-5, 17), textcoords="offset points")
    plt.annotate("same return, more risk → dominated", ((s_a + s_b) / 2, 2), xytext=(-55, -52), textcoords="offset points", arrowprops=dict(arrowstyle="->"))
    plt.axvline(s_m, linestyle="--", linewidth=1)
    plt.xlim(0.45, 1.55)
    plt.ylim(1.55, 2.45)
    plt.xlabel(r"Risk  $\sigma_p$")
    plt.ylabel(r"Expected return  $\bar r_p$")
    plt.title("PS4 Exercise 1: feasible set is horizontal; only the left endpoint is efficient")
    plt.grid(alpha=0.2)
    plt.tight_layout()
    plt.savefig(path, dpi=220, bbox_inches="tight")
    plt.close()


def save_two_fund(path: Path) -> None:
    s_t = 1 / math.sqrt(2)
    rf = 1.0
    slope = math.sqrt(2)
    x = np.linspace(0, 1.55, 300)
    y = rf + slope * x
    plt.figure(figsize=(7.5, 4.7))
    plt.plot(x, y, linewidth=2.5, label="capital allocation line")
    points = {
        "F: risk-free": (0, rf),
        "L: lender": (0.34, rf + slope * 0.34),
        "T: tangency / MVP": (s_t, 2.0),
        "B: borrower / leverage": (1.22, rf + slope * 1.22),
    }
    for name, (px, py) in points.items():
        plt.scatter([px], [py], s=55)
        dx, dy = (7, 8)
        if name.startswith("L"):
            dy = -28
        if name.startswith("B"):
            dx, dy = (-95, 8)
        plt.annotate(name, (px, py), xytext=(dx, dy), textcoords="offset points")
    # Two stylized indifference curves tangent to the line at lender/borrower choices.
    for x0, span in [(0.34, (0.08, 0.67)), (1.22, (0.86, 1.5))]:
        xx = np.linspace(span[0], span[1], 100)
        y0 = rf + slope * x0
        yy = y0 + slope * (xx - x0) + 1.05 * (xx - x0) ** 2
        plt.plot(xx, yy, linestyle="--", linewidth=1.2)
    plt.axvline(s_t, linestyle=":", linewidth=1)
    plt.xlabel(r"Risk  $\sigma_p$")
    plt.ylabel(r"Expected return  $\bar r_p$")
    plt.title("Two-fund separation: everyone combines F and the same tangency portfolio T")
    plt.grid(alpha=0.2)
    plt.legend(frameon=False, loc="upper left")
    plt.tight_layout()
    plt.savefig(path, dpi=220, bbox_inches="tight")
    plt.close()


def save_rate_cut(path: Path) -> None:
    s_t = 1 / math.sqrt(2)
    mu_t = 2.0
    rf_old = 1.0
    rf_new = 0.5
    old_slope = (mu_t - rf_old) / s_t
    new_slope = (mu_t - rf_new) / s_t
    x = np.linspace(0, 1.55, 300)
    plt.figure(figsize=(7.5, 4.6))
    plt.plot(x, rf_old + old_slope * x, linewidth=2.2, label=r"before: $r_f=1$")
    plt.plot(x, rf_new + new_slope * x, linestyle="--", linewidth=2.2, label=r"after cut: $r_f=0.5$")
    plt.scatter([s_t], [mu_t], s=70)
    plt.annotate("T", (s_t, mu_t), xytext=(8, 8), textcoords="offset points")
    plt.axvline(s_t, linestyle=":", linewidth=1)
    plt.annotate("lender zone\nold opportunity line is higher", (0.28, 1.25), xytext=(10, -55), textcoords="offset points", arrowprops=dict(arrowstyle="->"))
    plt.annotate("borrower zone\nnew opportunity line is higher", (1.23, 3.1), xytext=(-85, 15), textcoords="offset points", arrowprops=dict(arrowstyle="->"))
    plt.xlabel(r"Risk  $\sigma_p$")
    plt.ylabel(r"Expected return  $\bar r_p$")
    plt.title("A lower risk-free rate helps borrowers but hurts lenders in this exercise")
    plt.grid(alpha=0.2)
    plt.legend(frameon=False, loc="upper left")
    plt.tight_layout()
    plt.savefig(path, dpi=220, bbox_inches="tight")
    plt.close()


def save_flow(path: Path) -> None:
    # A compact visual flow using matplotlib text boxes.
    plt.figure(figsize=(8.2, 2.4))
    ax = plt.gca()
    ax.set_axis_off()
    xs = [0.08, 0.31, 0.54, 0.77]
    texts = [
        "Terminal wealth\nwrite it first",
        "Mean & variance\n(or expected utility)",
        "FOC → demand\n$X(P)$",
        "Market clearing\n$NX(P)=S$ → price $P$",
    ]
    for i, (x, text) in enumerate(zip(xs, texts)):
        ax.text(x, 0.52, text, ha="center", va="center", fontsize=11,
                bbox=dict(boxstyle="round,pad=0.55", fc="white", ec="0.35", lw=1.2))
        if i < len(xs) - 1:
            ax.annotate("", xy=(xs[i + 1] - 0.11, 0.52), xytext=(x + 0.11, 0.52),
                        arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.set_xlim(0, 0.88)
    ax.set_ylim(0, 1)
    plt.tight_layout()
    plt.savefig(path, dpi=220, bbox_inches="tight", transparent=True)
    plt.close()

GENERIC_CHART = ASSET / "generic_frontiers.png"
EX1_CHART = ASSET / "ps4_ex1_frontier.png"
TWO_FUND_CHART = ASSET / "two_fund_separation.png"
RATE_CUT_CHART = ASSET / "rf_cut.png"
FLOW_CHART = ASSET / "ps3_flow.png"

save_generic_frontier(GENERIC_CHART)
save_ex1_frontier(EX1_CHART)
save_two_fund(TWO_FUND_CHART)
save_rate_cut(RATE_CUT_CHART)
save_flow(FLOW_CHART)

# -----------------------------------------------------------------------------
# Document template
# -----------------------------------------------------------------------------
class StudyDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str):
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=LEFT,
            rightMargin=RIGHT,
            topMargin=TOP,
            bottomMargin=BOTTOM,
            title="금융론 1–7강 최종 참고본 — 교수님 시험 강조 + PS4 특수풀이",
            author="OpenAI",
            subject="Money, Banking and Finance A exam reference",
        )
        frame = Frame(LEFT, BOTTOM, CONTENT_W, PAGE_H - TOP - BOTTOM, id="normal", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="content", frames=frame, onPage=self._draw_page),
        ])

    def _draw_page(self, canv, doc):
        page = canv.getPageNumber()
        if page > 1:
            canv.saveState()
            canv.setStrokeColor(LINE)
            canv.setLineWidth(0.5)
            canv.line(LEFT, PAGE_H - 12 * mm, PAGE_W - RIGHT, PAGE_H - 12 * mm)
            canv.setFont("NanumGothic", 7.3)
            canv.setFillColor(MID)
            canv.drawString(LEFT, PAGE_H - 9 * mm, "금융론 1–7강 최종 참고본 · PS4 중심")
            canv.drawRightString(PAGE_W - RIGHT, 9 * mm, str(page))
            canv.line(LEFT, 12 * mm, PAGE_W - RIGHT, 12 * mm)
            canv.restoreState()


def cover_page(canv, doc):
    # Full-page cover decoration drawn under flowables.
    canv.saveState()
    canv.setFillColor(NAVY)
    canv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canv.setFillColor(BLUE)
    canv.circle(PAGE_W - 25 * mm, PAGE_H - 20 * mm, 38 * mm, fill=1, stroke=0)
    canv.setFillColor(TEAL)
    canv.circle(PAGE_W - 7 * mm, 17 * mm, 52 * mm, fill=1, stroke=0)
    canv.setFillColor(colors.Color(1, 1, 1, alpha=0.18))
    for y in [36, 49, 62, 75]:
        canv.roundRect(LEFT, y * mm, PAGE_W - LEFT - RIGHT, 8 * mm, 2 * mm, fill=1, stroke=0)
    canv.restoreState()


# -----------------------------------------------------------------------------
# Story
# -----------------------------------------------------------------------------
story: List = []

# Cover (use a frame-like table so it sits on navy background)
story.append(Spacer(1, 23 * mm))
story.append(P("금융론 1–7강<br/>최종 참고본", TITLE))
story.append(Spacer(1, 5 * mm))
story.append(P("교수님 시험 강조 + PS4 특수풀이 완전정리", SUBTITLE))
story.append(Spacer(1, 18 * mm))
cover_box = Table([
    [P("이 자료의 역할", ParagraphStyle("CoverBoxT", parent=BOX_TITLE, textColor=WHITE, fontSize=11.5, leading=16)),],
    [P("사진으로 올린 수업 필기 2장, PS4 원문, 강의 녹취에서 교수님이 직접 강조한 풀이 순서와 감점 포인트를 중심으로 재구성했다. PS4만 따로 보는 자료가 아니라, PS1–PS4를 시험 직전 한 번에 연결하는 ‘최종 참고본’이다.", ParagraphStyle("CoverBoxB", parent=BODY, textColor=WHITE, fontSize=10.2, leading=16)),],
], colWidths=[CONTENT_W])
cover_box.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.Color(1, 1, 1, alpha=0.13)),
    ("BOX", (0, 0), (-1, -1), 0.8, colors.Color(1, 1, 1, alpha=0.35)),
    ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ("TOPPADDING", (0, 0), (-1, -1), 9),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
]))
story.append(cover_box)
story.append(Spacer(1, 20 * mm))
story.append(P("핵심 한 줄", ParagraphStyle("CoverK", parent=BOX_TITLE, textColor=WHITE, fontSize=11)))
story.append(P("PS4는 ‘공식 암기’보다 <b>5단계 풀이를 끝까지 쓰고, 식에서 그래프를 뽑아내는 능력</b>이 중요하다.", ParagraphStyle("CoverQuote", parent=QUOTE, textColor=WHITE, fontSize=13.2, leading=20)))
story.append(Spacer(1, 22 * mm))
story.append(P("Money, Banking and Finance A · Lectures 1–7", ParagraphStyle("CoverFoot", parent=BODY_SMALL, textColor=WHITE)))
story.append(PageBreak())

# 1. Priority map
story += section_title("01 · 먼저 볼 것", "교수님 발언 기준 시험 우선순위", "‘어려운 수학’보다 반복 가능한 풀이 구조와 경제적 설명을 먼저 잡는다.")
story.append(callout(
    "결론",
    "<b>최우선은 PS4의 정석형 Markowitz 문제다.</b> 교수님은 PS4 유형이 출제하기 쉽고, 계산도 어렵지 않으며, Exercise 2–7은 같은 절차로 풀 수 있다고 여러 차례 강조했다. Exercise 1은 그 절차가 깨지는 유일한 특수형이라 수업에서 직접 길게 풀이했다.",
    PALE_RED,
    RED,
))
story.append(Spacer(1, 7))
priority_rows = [
    ["S", "PS4", "5단계 cookbook, Exercise 1 특수풀이, MVP, 그래프, 공매도 제약, 무위험자산, 2기금 분리, 금리 인하 판단"],
    ["A", "PS3", "최종부 → 평균·분산 → FOC → 수요 → 시장청산 → 균형가격. 경제적 직관까지."],
    ["B", "PS1·PS2", "일반균형의 반복 절차, ARA/RRA에서 CARA·CRRA 식별, 기대효용 비교와 wealth effect"],
]
story.append(data_table(["등급", "범위", "시험 직전 목표"], priority_rows, [18 * mm, 27 * mm, CONTENT_W - 45 * mm], 8.2))
story.append(Spacer(1, 7))
story.append(P("답안은 항상 다음 순서로 쓴다", H2))
answer_steps = [
    "① <b>조건 확인</b>: 확률, 수익률 단위, 공매도 허용 여부, 무위험자산 존재 여부",
    "② <b>정의와 식</b>: 무엇을 계산하는지 먼저 적기",
    "③ <b>계산</b>: 평균·분산·공분산·상관계수 → 포트폴리오 평균·분산",
    "④ <b>도출</b>: FOC·시장청산·가중치 제거 등 필요한 조작",
    "⑤ <b>그림과 직관</b>: 축, 끝점, 제약, 누가 지배되는지, 왜 그런지 한두 문장",
]
for s in answer_steps:
    story.append(bullet(s, strong=False))
story.append(Spacer(1, 5))
story.append(callout(
    "교수님이 실제로 보는 흔적",
    "정답 숫자만 맞는 것보다 <b>공분산 항을 쓴 뒤 0이라서 사라졌다고 표시</b>하고, 공매도 금지이면 곡선을 A·B에서 정확히 멈추며, 식을 도출한 뒤 그래프를 그렸다는 흔적을 남기는 것이 중요하다.",
    PALE_ORANGE,
    ORANGE,
))
story.append(PageBreak())

# 2. Course map
story += section_title("02 · 전체 지도", "1–7강은 네 개의 문제 구조로 연결된다", "강의 회차명을 억지로 외우지 말고, 어떤 입력에서 어떤 답을 뽑는지로 묶는다.")
map_rows = [
    ["일반균형 · PS1", "개별 최적화 → 수요 → 시장청산", "가격비율·균형배분·Edgeworth Box·Pareto 효율"],
    ["위험태도 · PS2", "효용의 곡률과 기대효용", "CARA/CRRA 식별·도박 수락 여부·확실성등가·wealth effect"],
    ["포트폴리오·가격 · PS3", "최종부 → FOC → 자산수요 → 시장청산", "최적 위험투자·균형가격·위험프리미엄·이질적 믿음과 거래량"],
    ["평균–분산 · PS4", "평균·분산·공분산 → frontier", "MVP·효율적 프런티어·Sharpe·무위험자산·2기금 분리"],
]
story.append(data_table(["묶음", "반복 구조", "최종 산출물"], map_rows, [39 * mm, 58 * mm, CONTENT_W - 97 * mm], 8.0))
story.append(Spacer(1, 9))
story.append(P("네 묶음을 관통하는 공통 논리", H2))
common_left = [
    P("<b>개인 단계</b>", H3),
    bullet("예산제약 또는 최종부를 먼저 쓴다."),
    bullet("목적함수의 FOC로 최적 선택이나 수요를 구한다."),
    bullet("위험이 있으면 평균뿐 아니라 분산·공분산을 반드시 반영한다."),
]
common_right = [
    P("<b>시장·그림 단계</b>", H3),
    bullet("시장청산으로 가격을 내생적으로 구한다."),
    bullet("그래프에서는 축·끝점·제약·접점을 먼저 표시한다."),
    bullet("마지막에 ‘왜’인지 위험프리미엄·분산효과로 설명한다."),
]
story.append(two_col(common_left, common_right))
story.append(Spacer(1, 8))
story.append(formula_card(
    "한 줄 연결식",
    r"\text{preferences and constraints}\;\longrightarrow\;\text{choice/demand}\;\longrightarrow\;\text{market clearing or frontier}\;\longrightarrow\;\text{price/welfare}",
    "PS1은 재화시장, PS3는 자산시장, PS4는 위험–수익 가능집합에 같은 사고방식을 적용한다.",
    PALE_TEAL,
))
story.append(PageBreak())

# 3. PS4 cookbook
story += section_title("03 · 최우선", "PS4 정석형 문제: 5단계 cookbook", "Exercise 2–7은 이 순서를 자동으로 쓸 수 있을 때까지 반복한다.")
steps = [
    ("STEP 0", "문제 조건 표시", "확률 πs, 수익률 단위, w의 범위, 공매도, 무위험자산을 문제지에 동그라미 친다."),
    ("STEP 1", "다섯 통계량", "A·B의 기대수익률 2개, 표준편차 2개, 공분산 1개를 계산한다."),
    ("STEP 2", "상관계수", "ρAB = Cov(A,B)/(σAσB). 1, 0, −1인지 먼저 확인한다."),
    ("STEP 3", "포트폴리오 평균·분산", "r̃p = wr̃A+(1−w)r̃B를 쓰고 평균과 분산을 구한다."),
    ("STEP 4", "w 제거", "평균식에서 w를 풀어 분산식에 대입해 σp와 r̄p의 관계를 만든다."),
    ("STEP 5", "그래프·효율성", "(σp,r̄p) 평면에 A·B부터 찍고, 제약을 지키며 frontier와 효율적인 부분을 표시한다."),
]
step_data = [[a, b, c] for a, b, c in steps]
story.append(data_table(["순서", "해야 할 일", "답안에 남길 흔적"], step_data, [23 * mm, 43 * mm, CONTENT_W - 66 * mm], 8.0))
story.append(Spacer(1, 8))
story.append(formula_card(
    "STEP 1–2 · 기본 통계",
    r"\bar r_i=\sum_s\pi_s r_{i,s},\quad \sigma_i^2=\sum_s\pi_s(r_{i,s}-\bar r_i)^2,\quad \sigma_{AB}=\sum_s\pi_s(r_{A,s}-\bar r_A)(r_{B,s}-\bar r_B),\quad \rho_{AB}=\frac{\sigma_{AB}}{\sigma_A\sigma_B}",
    "확률이 1/3이라고 자동으로 가정하지 않는다. 문제에 제시된 확률을 그대로 사용한다.",
))
story.append(Spacer(1, 6))
story.append(formula_card(
    "STEP 3 · 절대 생략하면 안 되는 식",
    r"\widetilde r_p=w\widetilde r_A+(1-w)\widetilde r_B,\quad \bar r_p=w\bar r_A+(1-w)\bar r_B,\quad \sigma_p^2=w^2\sigma_A^2+(1-w)^2\sigma_B^2+2w(1-w)\sigma_{AB}",
    "공분산이 0인 문제라도 마지막 항을 먼저 적고 ‘σAB=0이므로 0’이라고 지운다.",
    PALE_ORANGE,
))
story.append(Spacer(1, 6))
story.append(callout(
    "시험 중 자기검산 신호",
    "교수님은 계산이 쉬운 문제를 만들겠다고 했고, 상관계수가 정확히 <b>1, 0, −1</b>로 떨어지는 형태를 특히 언급했다. 0.4나 0.8이 나오면 무조건 오답이라는 뜻은 아니지만, 그대로 밀고 가기 전에 평균·분산·공분산 계산을 다시 확인한다.",
    PALE_RED,
    RED,
))
story.append(PageBreak())

# 4. Generic shapes
story += section_title("04 · 그래프", "상관계수와 공매도 제약이 모양을 결정한다", "그림을 외워서 찍지 말고, 도출한 식과 조건에서 그린다.")
story.append(add_image(GENERIC_CHART, width=165 * mm, max_h=95 * mm))
story.append(Spacer(1, 5))
shape_rows = [
    ["ρAB=1", "완전 양의 상관", "분산효과가 없다. A와 B를 잇는 직선형."],
    ["ρAB=0", "무상관", "곡선이 왼쪽으로 휘며 A 단독보다 위험이 낮아질 수 있다."],
    ["ρAB=−1", "완전 음의 상관", "적절한 비율에서 σp=0인 포트폴리오가 가능하다."],
]
story.append(data_table(["신호", "의미", "그래프 해석"], shape_rows, [28 * mm, 39 * mm, CONTENT_W - 67 * mm], 8.1))
story.append(Spacer(1, 7))
story.append(two_col(
    [P("<b>공매도 금지</b>", H3), bullet("0≤w≤1"), bullet("가능집합은 A와 B 사이에서 끝난다."), bullet("끝점을 넘어 그리면 제약을 이해하지 못한 답처럼 보인다.")],
    [P("<b>공매도 허용</b>", H3), bullet("w<0 또는 w>1 가능"), bullet("A 또는 B를 공매도하므로 frontier가 끝점 밖으로 연장된다."), bullet("효율적 부분과 단순 가능집합을 구분한다.")],
))
story.append(Spacer(1, 6))
story.append(callout(
    "일반형에서의 효율적 프런티어",
    "최소분산점(MVP)을 기준으로 같은 위험에서 더 높은 기대수익률을 주는 <b>위쪽 가지</b>만 효율적이다. 다만 Exercise 1처럼 모든 포트폴리오의 기대수익률이 같으면 예외적으로 MVP 한 점만 효율적이다.",
    PALE_TEAL,
    TEAL,
))
story.append(PageBreak())

# 5. Ex1 moments
story += section_title("05 · PS4 Exercise 1", "왜 이 문제만 ‘특수형’인가", "사진 첫 장의 계산을 정돈한 버전이다. 이 문제를 이해하면 정석형과 예외형을 동시에 구분할 수 있다.")
ex1_rows = [
    ["확률", "1/3", "1/3", "1/3"],
    ["A 수익률", "1", "2", "3"],
    ["B 수익률", "3", "0", "3"],
]
story.append(data_table(["", "State 1", "State 2", "State 3"], ex1_rows, [34 * mm, 42 * mm, 42 * mm, 42 * mm], 8.5))
story.append(Spacer(1, 7))
story.append(callout(
    "단위 주의",
    "문제의 수익률 3은 계산상 <b>3 그대로</b>, 즉 300%다. 현실적으로 큰 값이지만 계산을 단순하게 하려고 설정한 숫자이므로 0.03으로 바꾸면 안 된다.",
    PALE_ORANGE,
    ORANGE,
))
story.append(Spacer(1, 8))
story.append(P("STEP 1 · 기대수익률과 위험", H2))
story.append(formula_card(
    "기대수익률",
    r"\bar r_A=\frac{1+2+3}{3}=2,\qquad \bar r_B=\frac{3+0+3}{3}=2",
    "두 자산의 기대수익률이 정확히 같다. 이것이 특수형의 출발점이다.",
))
story.append(Spacer(1, 5))
story.append(formula_card(
    "분산과 표준편차",
    r"\sigma_A^2=\frac{(1-2)^2+(2-2)^2+(3-2)^2}{3}=\frac{2}{3},\quad \sigma_A=\sqrt{\frac{2}{3}};\qquad \sigma_B^2=\frac{(3-2)^2+(0-2)^2+(3-2)^2}{3}=2,\quad \sigma_B=\sqrt2",
    "A가 B보다 변동성이 작지만, A만 보유하는 것이 최소위험이라는 뜻은 아니다. 분산투자 효과를 계산해야 한다.",
    PALE_BLUE,
))
story.append(Spacer(1, 5))
story.append(formula_card(
    "공분산과 상관계수",
    r"\sigma_{AB}=\frac{(-1)(1)+(0)(-2)+(1)(1)}{3}=0,\qquad \rho_{AB}=\frac{0}{\sqrt{2/3}\sqrt2}=0",
    "상관계수 0이므로 포트폴리오 분산식의 교차항이 사라진다. ‘원래 없는 항’이 아니다.",
    PALE_GREEN,
))
story.append(PageBreak())

# 6. Ex1 optimization
story += section_title("06 · PS4 Exercise 1", "평균식에서 w를 풀 수 없으면 MVP를 직접 찾는다", "정석형 STEP 4가 왜 깨지는지와 대체 풀이를 함께 외운다.")
story.append(formula_card(
    "포트폴리오 평균",
    r"\bar r_p=w\bar r_A+(1-w)\bar r_B=2w+2(1-w)=2",
    "w가 무엇이든 기대수익률은 2다.",
))
story.append(Spacer(1, 5))
story.append(formula_card(
    "포트폴리오 분산",
    r"\sigma_p^2=w^2\frac{2}{3}+(1-w)^2\,2+2w(1-w)\underbrace{\sigma_{AB}}_{0}=\frac{2}{3}w^2+2(1-w)^2",
    "공분산 항을 먼저 쓴 뒤 0으로 처리하는 형식을 답안에 남긴다.",
    PALE_ORANGE,
))
story.append(Spacer(1, 7))
story.append(callout(
    "왜 w 제거가 불가능한가",
    "일반형에서는 w=(r̄p−r̄B)/(r̄A−r̄B)로 바꾸지만, 여기서는 분모가 r̄A−r̄B=0이다. 또한 r̄p−r̄B=0이어서 0/0이 된다. <b>따라서 평균식과 분산식 사이에서 w를 제거하는 정석 STEP 4를 사용할 수 없다.</b>",
    PALE_RED,
    RED,
))
story.append(Spacer(1, 8))
story.append(P("MVP를 찾는 두 가지 허용 풀이", H2))
left_method = [
    P("<b>방법 1 · 미분</b>", H3),
    equation(r"\frac{d\sigma_p^2}{dw}=\frac{4}{3}w-4(1-w)=0", width=72 * mm, fontsize=16),
    equation(r"w_A^*=\frac34,\qquad w_B^*=\frac14", width=65 * mm, fontsize=17),
    P("표준적인 방법. 분산을 w의 볼록한 이차함수로 보고 FOC를 쓴다.", BODY_SMALL),
]
right_method = [
    P("<b>방법 2 · 완전제곱</b>", H3),
    equation(r"\sigma_p^2=\frac83\left(w-\frac34\right)^2+\frac12", width=72 * mm, fontsize=16),
    equation(r"\min\sigma_p^2=\frac12\quad\text{at}\quad w=\frac34", width=68 * mm, fontsize=16),
    P("수업에서 학생 풀이로 소개된 빠른 방법. 제곱항이 0일 때 최소다.", BODY_SMALL),
]
story.append(two_col(left_method, right_method))
story.append(Spacer(1, 7))
story.append(formula_card(
    "MVP 최종값",
    r"w_A=\frac34,\quad w_B=\frac14,\quad \bar r_{MVP}=2,\quad \sigma_{MVP}^2=\frac12,\quad \sigma_{MVP}=\frac{1}{\sqrt2}",
    "반드시 ‘분산 1/2’와 ‘표준편차 1/√2’를 구분한다.",
    PALE_GREEN,
))
story.append(PageBreak())

# 7. Ex1 graph
story += section_title("07 · PS4 Exercise 1", "무위험자산이 없을 때 효율적 프런티어는 ‘한 점’", "사진 첫 장 아래쪽의 수평 그래프를 정확한 좌표로 다시 그렸다.")
story.append(add_image(EX1_CHART, width=165 * mm, max_h=92 * mm))
story.append(Spacer(1, 6))
story.append(P("판단 논리", H2))
for text in [
    "모든 A–B 포트폴리오의 기대수익률은 2로 같다.",
    "w=3/4일 때 위험이 가장 낮다: σ=1/√2.",
    "MVP보다 오른쪽의 모든 포트폴리오는 <b>같은 수익률인데 위험만 더 크다.</b>",
    "따라서 가능집합은 수평선분이지만, 효율적 프런티어는 MVP 한 점뿐이다.",
]:
    story.append(bullet(text))
story.append(Spacer(1, 7))
story.append(callout(
    "Part (a) 모범답안 골격",
    "‘r̄A=r̄B=2이고 ρAB=0이다. 따라서 r̄p=2이며 σp²=(2/3)w²+2(1−w)². 이를 최소화하면 wA=3/4, wB=1/4이고 σMVP=1/√2다. 모든 포트폴리오의 기대수익률이 같으므로 MVP 이외는 동일 수익률에서 더 위험하여 지배된다. 따라서 효율적 프런티어는 (1/√2,2) 한 점이다.’",
    PALE_BLUE,
    BLUE,
))
story.append(Spacer(1, 7))
story.append(callout(
    "자주 하는 잘못된 그림",
    "A와 B의 기대수익률이 같다고 A–B 사이만 직선으로 잇고 끝내면 분산효과를 놓친다. 먼저 분산을 최소화하면 A보다 더 왼쪽에 MVP가 나온다는 사실을 계산으로 보여야 한다.",
    PALE_ORANGE,
    ORANGE,
))
story.append(PageBreak())

# 8. Two-fund separation
story += section_title("08 · PS4 Exercise 1", "무위험자산이 들어오면: 접점포트폴리오와 2기금 분리", "사진 두 번째 장의 T·무차별곡선·대출/차입 그림을 깔끔하게 재구성했다.")
story.append(add_image(TWO_FUND_CHART, width=165 * mm, max_h=97 * mm))
story.append(Spacer(1, 5))
story.append(formula_card(
    "이 문제의 자본배분선",
    r"F=(0,1),\qquad T=\left(\frac{1}{\sqrt2},2\right),\qquad \bar r_p=r_f+\frac{\bar r_T-r_f}{\sigma_T}\sigma_p=1+\sqrt2\,\sigma_p",
    "위험자산 효율집합이 T 한 점이므로, 무위험점 F와 T를 잇고 차입 허용이면 T 오른쪽으로 연장한다.",
))
story.append(Spacer(1, 7))
alloc_rows = [
    ["F와 T 사이", "0<λ<1", "무위험자산 + T", "순대출자: 국채를 보유하고 위험노출을 줄인다."],
    ["T", "λ=1", "T 100%", "A:B=3:1의 위험자산 포트폴리오만 보유"],
    ["T 오른쪽", "λ>1", "T + 무위험자산 음의 비중", "순차입자: 무위험금리로 빌려 레버리지를 건다."],
]
story.append(data_table(["위치", "T 비중", "보유", "경제적 의미"], alloc_rows, [28 * mm, 22 * mm, 45 * mm, CONTENT_W - 95 * mm], 7.8))
story.append(Spacer(1, 7))
story.append(callout(
    "2기금 분리정리의 시험용 문장",
    "투자자의 위험회피도가 달라도 모두 <b>같은 접점포트폴리오 T</b>와 무위험자산의 조합을 선택한다. 이 문제에서 T 내부의 위험자산 비율은 언제나 A:B=3:1이다. 사람마다 달라지는 것은 A와 B의 비율이 아니라 <b>T 전체와 무위험자산 사이의 비율</b>이다.",
    PALE_GREEN,
    GREEN,
))
story.append(PageBreak())

# 9. T/F and rate cut
story += section_title("09 · PS4 Exercise 1", "Part (c)·(d): 설명형 함정", "숫자 계산 뒤에 2기금 분리와 대출자·차입자 해석을 붙이는 문제다.")
story.append(P("Part (c) · ‘더 위험회피적일수록 B 비중은 낮고 A 비중은 높다’", H2))
story.append(callout(
    "정답: False",
    "위험회피도가 높아지면 투자자는 T의 총비중을 줄이고 무위험자산 비중을 늘린다. 그러나 T 안의 A:B=3:1 비율은 바뀌지 않는다. 따라서 ‘위험회피도에 따라 A와 B의 상대비율이 달라진다’는 주장은 2기금 분리정리에 어긋난다.",
    PALE_RED,
    RED,
))
story.append(Spacer(1, 8))
story.append(P("Part (d) · ‘금리 인하는 Sharpe ratio를 높이므로 모든 투자자가 환영한다’", H2))
story.append(callout(
    "정답: Can’t tell / 투자자에 따라 다름",
    "Sharpe ratio가 올라간다는 사실만으로 모든 사람의 후생이 올라간다고 결론내릴 수 없다. 이 문제에서는 금리 인하 전후의 직선이 T에서 교차한다. T 왼쪽의 순대출자는 안전자산 수익률 하락으로 불리하고, T 오른쪽의 순차입자는 차입비용 하락으로 유리하다. T만 보유한 투자자는 그대로다.",
    PALE_RED,
    RED,
))
story.append(Spacer(1, 6))
story.append(add_image(RATE_CUT_CHART, width=165 * mm, max_h=93 * mm))
story.append(Spacer(1, 4))
story.append(P("<b>시험용 한 문장:</b> ‘금리 인하가 자본배분선의 기울기를 높이더라도, 대출자와 차입자에게 미치는 소득·비용 효과가 반대이므로 모든 투자자가 더 나아진다고 할 수 없다.’", BODY))
story.append(PageBreak())

# 10. Mistakes
story += section_title("10 · 감점 방지", "PS4에서 점수를 잃는 12가지", "계산을 아는 것과 채점 가능한 답안을 쓰는 것은 다르다.")
mistakes = [
    ("공분산 항 누락", "분산식을 w²σA²+(1−w)²σB²까지만 쓰는 것. 2w(1−w)σAB를 적고 0이면 그때 지운다."),
    ("분산·표준편차 혼동", "그래프의 가로축은 σp, 목적식에는 σp²가 자주 나온다. 마지막에 제곱근을 확인한다."),
    ("확률 자동 가정", "state가 3개라고 무조건 1/3이 아니다. 교수님이 상관계수를 예쁘게 만들려고 확률을 바꿀 수 있다고 말했다."),
    ("수익률 단위 변경", "3을 0.03으로 바꾸지 않는다. 문제의 note를 그대로 따른다."),
    ("공매도 제약 무시", "금지이면 0≤w≤1이고 곡선은 끝점에서 멈춘다."),
    ("식 없이 그림 암기", "ρ 모양만 외워 그리지 말고 r̄p–σp 관계를 도출한 뒤 그린다."),
    ("축 반대로 그리기", "가로 σp, 세로 r̄p. A·B 좌표부터 찍는다."),
    ("가능집합=효율적 프런티어", "MVP 아래 가지 또는 지배되는 부분을 효율적이라고 칠하지 않는다."),
    ("Exercise 1에서 0으로 나누기", "r̄A=r̄B이면 평균식으로 w를 풀지 말고 분산을 직접 최소화한다."),
    ("False만 쓰기", "PS4의 판단형은 반드시 이론명과 인과관계를 덧붙인다."),
    ("상태별 지배와 MV 지배 혼동", "state-by-state dominance는 모든 상태를 보지만 mean–variance는 평균과 분산만 본다."),
    ("로그효용의 정의역 무시", "PS4 Exercise 7에서는 모든 상태의 최종부가 양수인지 확인한다."),
]
rows = [[str(i + 1), a, b] for i, (a, b) in enumerate(mistakes)]
story.append(data_table(["#", "실수", "교정"], rows, [10 * mm, 39 * mm, CONTENT_W - 49 * mm], 7.7))
story.append(Spacer(1, 7))
story.append(callout(
    "답안 끝의 경제적 직관",
    "‘상관이 낮아져 분산효과가 커진다’, ‘위험이 커져 요구 위험프리미엄이 올라간다’, ‘무위험자산 대비 초과수익률이 달라진다’, ‘제약 완화로 선택집합이 넓어진다’ 중 해당 문장을 반드시 붙인다.",
    PALE_TEAL,
    TEAL,
))
story.append(PageBreak())

# 11. Ex 2-7 map
story += section_title("11 · 연습문제 전이", "PS4 Exercise 2–7에서 먼저 찾아야 할 숫자 신호", "정답을 외우기보다, 상관계수와 제약을 보고 문제 유형을 분류한다.")
transfer_rows = [
    ["Ex.2", "ρAB=−1", "완전 음의 상관. σp=0 가능점, 공매도 허용/금지에 따른 frontier 절단, 효용최적점 비교."],
    ["Ex.3", "ρAB=0", "정석 5단계. MVP 보너스: wA=3/4, wB=1/4, r̄MVP=5/4, σMVP=1/√2."],
    ["Ex.4", "ρAB=1", "직선형 위험자산 frontier. Sharpe ratio 비교. rf가 5.5→4.5로 내려가면 최적 위험자산이 바뀔 수 있음."],
    ["Ex.5", "ρAB=−1", "무위험 조합 가능. B만 또는 둘 다 공매도 허용할 때 선택집합·후생이 어떻게 넓어지는지 그림."],
    ["Ex.6", "A–B는 ρ=−1", "매우 위험회피적인 투자자의 비중 판단. B를 state-by-state 우월한 C로 바꿔도 MV 평가가 역설을 낼 수 있음."],
    ["Ex.7", "ρAB=1", "직선형 frontier + 로그효용. MVP와 효용최적점은 다를 수 있고, 모든 상태에서 최종부>0 확인."],
]
story.append(data_table(["문제", "첫 신호", "핵심 과업"], transfer_rows, [19 * mm, 35 * mm, CONTENT_W - 54 * mm], 7.8))
story.append(Spacer(1, 8))
story.append(P("Exercise 4에서 금리 변화가 특별히 중요한 이유", H2))
story.append(formula_card(
    "Sharpe ratio",
    r"SR_i=\frac{\bar r_i-r_f}{\sigma_i}",
    "rf가 바뀌면 분자와 자본배분선의 절편·기울기가 함께 바뀐다. 따라서 기존 접점포트폴리오를 그대로 둔다고 가정하면 안 되고, 각 후보의 Sharpe ratio를 다시 비교한다.",
    PALE_BLUE,
))
story.append(Spacer(1, 6))
story.append(callout(
    "Exercise 6의 역설을 어떻게 설명할까",
    "C가 B보다 모든 상태에서 높은 수익을 주는데도 mean–variance 그림에서 어떤 투자자가 불리해 보일 수 있다. 이는 평균–분산 기준이 분포의 모든 상태와 효용을 보지 않고 평균과 분산 두 숫자로만 요약하기 때문에 생기는 <b>모형의 한계</b>다.",
    PALE_ORANGE,
    ORANGE,
))
story.append(PageBreak())

# 12. PS1
story += section_title("12 · PS1", "일반균형: 개인 최적화에서 시장 전체 가격까지", "PS4만 보다가 잊기 쉬운 전반부 기본형. 순서가 핵심이다.")
story.append(formula_card(
    "개별 예산제약",
    r"p_1c_{i1}+p_2c_{i2}=p_1e_{i1}+p_2e_{i2}",
    "소비자의 소득은 초기부존의 시장가치다. 예산선을 쓸 때 우변을 빠뜨리지 않는다.",
))
story.append(Spacer(1, 6))
story.append(formula_card(
    "내부해의 접선조건",
    r"MRS_{i,12}=\frac{\partial U_i/\partial c_{i1}}{\partial U_i/\partial c_{i2}}=\frac{p_1}{p_2}",
    "FOC와 예산제약을 함께 풀어 개별 수요함수를 구한다.",
    PALE_TEAL,
))
story.append(Spacer(1, 7))
ps1_steps = [
    "각 소비자의 효용함수와 초기부존을 읽는다.",
    "예산제약을 세우고 Lagrangian·FOC로 수요함수를 구한다.",
    "시장청산 Σici,j=Σiei,j를 적용해 가격비율 p1/p2를 구한다.",
    "한 가격을 1로 정규화하고 균형배분을 계산한다.",
    "Edgeworth Box에서 초기점 I, 균형점 E, 예산선 기울기 −p1/p2를 표시한다.",
    "contract curve는 MRSA=MRSB로 구하고, 경쟁균형의 Pareto 효율성을 설명한다.",
]
for s in ps1_steps:
    story.append(bullet(s))
story.append(Spacer(1, 7))
story.append(callout(
    "한 줄 암기",
    "<b>최적화 → 수요 → 시장청산 → 가격비율 → 배분 → 그림.</b> PS3의 ‘포트폴리오 문제 → 자산수요 → 시장청산 → 자산가격’과 같은 골격이다.",
    PALE_GREEN,
    GREEN,
))
story.append(Spacer(1, 8))
story.append(P("Edgeworth Box 체크", H2))
edge_rows = [
    ["예산선", "초기부존점과 균형점을 지나며 기울기는 −p1/p2"],
    ["계약곡선", "두 소비자의 MRS가 같은 Pareto 효율 배분들의 집합"],
    ["경쟁균형", "예산제약 아래 각자 최적이며 모든 시장에서 수요=공급"],
    ["공정성", "Pareto 효율은 낭비가 없다는 뜻이지 반드시 공정하다는 뜻은 아님"],
]
story.append(data_table(["요소", "의미"], edge_rows, [38 * mm, CONTENT_W - 38 * mm], 8.2))
story.append(PageBreak())

# 13. PS2
story += section_title("13 · PS2", "위험태도: 효용함수를 식별한 뒤 기대효용을 비교", "도박 문제는 숫자보다 ‘어떤 효용함수인가’를 먼저 찾는다.")
story.append(two_col(
    [
        formula_card("절대위험회피도", r"ARA(W)=-\frac{U''(W)}{U'(W)}", "상수 ν이면 CARA: U(W)=−e^{−νW}.", PALE_BLUE, width=(CONTENT_W - 6 * mm) / 2),
        Spacer(1, 5),
        P("<b>CARA 핵심</b>", H3),
        bullet("절대 위험투자액이 초기부와 무관한 no wealth effect."),
        bullet("초기부가 양변에서 지수항으로 소거되는 문제를 인식."),
    ],
    [
        formula_card("상대위험회피도", r"RRA(W)=-\frac{W U''(W)}{U'(W)}", "상수 γ이면 CRRA. γ=1일 때 log U(W)=ln W.", PALE_TEAL, width=(CONTENT_W - 6 * mm) / 2),
        Spacer(1, 5),
        P("<b>CRRA 핵심</b>", H3),
        bullet("최적 위험투자액은 부에 비례하고 비중이 안정적."),
        bullet("log/power 효용은 W>0 정의역을 확인."),
    ],
))
story.append(Spacer(1, 8))
story.append(P("기대효용 문제 4단계", H2))
for s in [
    "① 주어진 ARA/RRA 조건에서 효용함수 형태를 식별한다.",
    "② 각 선택의 상태별 최종부를 쓴다.",
    "③ ΣsπsU(Ws)와 확실한 선택의 U(Wcertain)를 비교한다.",
    "④ 위험회피·중립·선호의 곡률과 wealth effect로 문장 설명을 붙인다.",
]:
    story.append(bullet(s))
story.append(Spacer(1, 7))
story.append(callout(
    "Jensen 직관",
    "U''<0인 위험회피자는 같은 기대부를 주는 공정한 도박보다 확실한 부를 선호한다. 다만 서로 다른 주관확률을 가진 두 사람이 같은 내기에 동시에 참여할 수 있으므로, ‘제로섬 내기이니 절대 거래하지 않는다’고 단정하면 안 된다.",
    PALE_ORANGE,
    ORANGE,
))
story.append(PageBreak())

# 14. PS3
story += section_title("14 · PS3", "포트폴리오와 균형자산가격: 최종부를 먼저 써라", "수업에서 반복된 해결 순서를 공식과 직관으로 압축한다.")
story.append(add_image(FLOW_CHART, width=166 * mm, max_h=47 * mm))
story.append(Spacer(1, 7))
story.append(formula_card(
    "위험자산 1개 + 무위험자산",
    r"\widetilde Y_1=(1+\widetilde r)a+(1+r_f)(Y_0-a)",
    "a는 위험자산에 투자한 금액. 최종부를 쓴 뒤 평균과 분산 또는 기대효용을 계산한다.",
))
story.append(Spacer(1, 5))
story.append(formula_card(
    "CARA–normal의 certainty-equivalent 문제",
    r"\max_a\; (\bar r-r_f)a+(1+r_f)Y_0-\frac12\nu a^2\sigma_r^2\quad\Longrightarrow\quad a^*=\frac{\bar r-r_f}{\nu\sigma_r^2}",
    "초과기대수익률이 커지면 a*↑, 위험회피도·분산이 커지면 a*↓. CARA라서 Y0와 무관하다.",
    PALE_GREEN,
))
story.append(Spacer(1, 6))
story.append(P("균형자산가격 cookbook", H2))
story.append(formula_card(
    "수요함수",
    r"\widetilde Y_1=\widetilde\delta X+(1+r_f)(Y_0-PX),\qquad X(P)=\frac{\bar\delta-(1+r_f)P}{\nu\sigma_\delta^2}",
    "P를 주어진 것으로 보고 투자자의 최적 X를 먼저 구한다.",
))
story.append(Spacer(1, 5))
story.append(formula_card(
    "시장청산과 가격",
    r"NX(P)=S\quad\Longrightarrow\quad P=\frac{\bar\delta-\nu\sigma_\delta^2(S/N)}{1+r_f}",
    "가격 = 기대현금흐름 − 위험프리미엄을 무위험금리로 할인한 값.",
    PALE_BLUE,
))
story.append(Spacer(1, 6))
comparative = [
    ["δ̄↑", "P↑", "기대현금흐름이 커져 더 높은 가격을 지불"],
    ["rf↑", "P↓", "할인율 상승 + 무위험자산의 상대매력 상승"],
    ["ν↑ 또는 σδ²↑", "P↓", "더 큰 위험프리미엄 요구"],
    ["S↑", "P↓", "고정 공급이 늘어 시장청산가격 하락"],
    ["N↑", "P↑", "1인당 부담 위험 S/N이 줄어 위험프리미엄 하락"],
]
story.append(data_table(["변화", "가격", "직관"], comparative, [31 * mm, 25 * mm, CONTENT_W - 56 * mm], 8.0))
story.append(PageBreak())

# 15. PS3 beliefs + exam scope
story += section_title("15 · PS3", "이질적 믿음·거래량과 시험 범위 감각", "기본 1자산 모형을 확실히 한 뒤, 믿음 차이 문제를 연결한다.")
story.append(formula_card(
    "낙관론자·비관론자의 균형가격",
    r"P=\frac{\alpha\bar\delta_H+(1-\alpha)\bar\delta_L-\nu\sigma^2(S/N)}{1+r_f}",
    "시장 평균 믿음에서 위험프리미엄을 뺀 뒤 할인한다.",
))
story.append(Spacer(1, 6))
story.append(formula_card(
    "시장 전체 거래량",
    r"V=\frac{N\alpha(1-\alpha)(\bar\delta_H-\bar\delta_L)}{\nu\sigma^2}",
    "α=1/2에서 가장 크고, 믿음 차이가 클수록·위험회피가 작을수록·자신감이 높을수록 거래량이 크다.",
    PALE_TEAL,
))
story.append(Spacer(1, 8))
story.append(callout(
    "교수님 수업 발언에서 잡을 범위",
    "여러 위험자산을 행렬·벡터로 푸는 일반형은 50–60분 시험에서 현실적으로 내기 어렵다고 언급했다. 반면 <b>최종부를 쓰고 평균·분산을 구한 뒤 FOC로 투자액을 구하는 기본형</b>, 그리고 <b>1자산 수요를 구해 시장청산으로 가격을 얻는 모형</b>은 충분히 출제 가능한 수준으로 봤다.",
    PALE_RED,
    RED,
))
story.append(Spacer(1, 8))
story.append(P("PS3 감점 방지", H2))
for s in [
    "처음부터 숫자를 넣지 말고 가능한 한 문자로 일반형을 푼 뒤 마지막에 수치대입한다.",
    "투자 ‘금액’ a와 주식 ‘수량’ X의 단위를 혼동하지 않는다.",
    "두 위험자산이면 분산에 2AB·Cov 항이 반드시 들어간다.",
    "상관이 양(+)이면 분산효과가 약해지고, 음(−)이면 두 자산을 함께 보유할 유인이 커진다.",
]:
    story.append(bullet(s))
story.append(PageBreak())

# 16. Final checklist
story += section_title("16 · 마지막 회독", "시험 직전 30분 루트와 자가진단", "아래 질문에 식과 그림 없이 말로 답할 수 있으면, 그다음 빈 종이에 직접 써본다.")
route_rows = [
    ["0–10분", "PS4 5단계와 평균·분산·공분산 공식을 빈 종이에 재현"],
    ["10–18분", "Exercise 1: 2, 2/3, 2, 0, 3/4, 1/2, 1/√2를 유도"],
    ["18–23분", "MVP 한 점, F–T 직선, lender/borrower, rf cut 두 직선 그리기"],
    ["23–27분", "PS3 수요 X(P)와 균형가격 P를 유도하고 비교정태 말하기"],
    ["27–30분", "PS1 순서와 CARA/CRRA 차이 구두 점검"],
]
story.append(data_table(["시간", "할 일"], route_rows, [30 * mm, CONTENT_W - 30 * mm], 8.4))
story.append(Spacer(1, 8))
story.append(P("자가진단 10문항", H2))
checks = [
    "포트폴리오 분산의 교차항을 아무것도 보지 않고 쓸 수 있는가?",
    "상관계수 1, 0, −1이 frontier에 주는 차이를 설명할 수 있는가?",
    "r̄A=r̄B이면 왜 w 제거가 실패하는가?",
    "Exercise 1의 MVP 비중·분산·표준편차를 각각 구분해 말할 수 있는가?",
    "왜 Exercise 1의 효율적 프런티어는 한 점인가?",
    "2기금 분리에서 투자자마다 같고 다른 것이 무엇인가?",
    "금리 인하가 lender와 borrower에게 반대 효과를 주는 이유는?",
    "PS1에서 개별 최적화 뒤 무엇을 시장청산하는가?",
    "CARA와 CRRA의 wealth effect 차이는?",
    "PS3에서 자산수요를 균형가격으로 바꾸는 마지막 조건은?",
]
for i, q in enumerate(checks, 1):
    story.append(P(f"<b>{i:02d}.</b> {q}", BODY))
story.append(Spacer(1, 8))
story.append(callout(
    "최종 답안 원칙",
    "공식만 쓰지 말고 <b>조건 → 식 → 계산 → 그래프 → 경제적 직관</b>의 순서를 지킨다. 특히 PS4는 맞는 그림 하나가 계산과 이론을 동시에 보여주는 답안이 된다.",
    PALE_GREEN,
    GREEN,
))
story.append(Spacer(1, 9))
story.append(P("자료 반영 범위", H2))
story.append(P("MBF lecture notes 1–4, Problem Sets 1–4 및 해설, PS4 exercise-session 강의 녹취, 사용자가 업로드한 손필기 사진 2장을 바탕으로 정리했다. 손필기 사진은 원본을 삽입하지 않고 계산과 그래프를 읽기 쉬운 형태로 다시 그렸다.", BODY_SMALL))

# Build with custom first page background.
doc = StudyDocTemplate(str(PDF_PATH))
# BaseDocTemplate does not expose onFirstPage in build; temporarily use a page callback wrapper.
original_draw = doc._draw_page

def draw_page(canv, d):
    if canv.getPageNumber() == 1:
        cover_page(canv, d)
    else:
        original_draw(canv, d)

for template in doc.pageTemplates:
    template.onPage = draw_page

doc.build(story)

# Validation
reader = PdfReader(str(PDF_PATH))
page_count = len(reader.pages)
size = PDF_PATH.stat().st_size
if page_count < 14:
    raise RuntimeError(f"Unexpectedly short PDF: {page_count} pages")
if size < 150_000:
    raise RuntimeError(f"Unexpectedly small PDF: {size} bytes")

manifest = OUT / "manifest.txt"
manifest.write_text(
    f"file={PDF_PATH.name}\npages={page_count}\nbytes={size}\nstatus=validated\n",
    encoding="utf-8",
)
print(f"Created {PDF_PATH} ({page_count} pages, {size:,} bytes)")
