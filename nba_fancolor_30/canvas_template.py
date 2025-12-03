# nba_fancolor_30/canvas_template.py

from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont

from .data import NUM_COLS, TEAMS


def build_base_template(
    cell_size: int = 115,
    bg_color: str = "#ffffff",
    circle_color: str = "#000000",
) -> Image.Image:
    """Build a base image with 30 circles and team abbreviations."""

    cols = NUM_COLS
    rows = (len(TEAMS) + cols - 1) // cols

    width = cols * cell_size
    height = rows * cell_size

    extra_bottom = 20
    img = Image.new("RGB", (width, height + extra_bottom), bg_color)
    draw = ImageDraw.Draw(img)

    # Slightly larger font for full team name below circle (balanced for export)
    font_name = _get_font(int(cell_size * 0.16))

    circle_margin = int(cell_size * 0.25)
    name_margin_top = int(cell_size * 0.05)

    for idx, team in enumerate(TEAMS):
        row = idx // cols
        col = idx % cols

        name = team["name"]
        team_color = team["color"]

        # Circle bounds
        x0 = col * cell_size + circle_margin
        y0 = row * cell_size + circle_margin
        x1 = (col + 1) * cell_size - circle_margin
        y1 = (row * cell_size + cell_size) - circle_margin  # or keep your original y1
        # If you didn't change y1 before, just keep your original calculation.

        # Circle outline in team color
        draw.ellipse((x0, y0, x1, y1), outline=circle_color, width=3)

        # ---------- Two-line team name under the circle ----------

        # Split into words
        words = name.split()

        if len(words) == 1:
            line1 = name
            line2 = ""
        elif len(words) == 2:
            line1, line2 = words
        else:
            # Put all but last word on line 1, last word on line 2
            line1 = " ".join(words[:-1])
            line2 = words[-1]

        center_x = (col + 0.5) * cell_size
        line_spacing = 2  # small gap between the two lines

        # First line
        bbox1 = draw.textbbox((0, 0), line1, font=font_name)
        w1 = bbox1[2] - bbox1[0]
        h1 = bbox1[3] - bbox1[1]

        line1_y = y1 + name_margin_top
        draw.text(
            (center_x - w1 / 2, line1_y),
            line1,
            fill="#000000",
            font=font_name,
        )

        # Second line (if any)
        if line2:
            bbox2 = draw.textbbox((0, 0), line2, font=font_name)
            w2 = bbox2[2] - bbox2[0]
            h2 = bbox2[3] - bbox2[1]

            line2_y = line1_y + h1 + line_spacing
            draw.text(
                (center_x - w2 / 2, line2_y),
                line2,
                fill="#000000",
                font=font_name,
            )

    return img


def _get_font(size: int) -> ImageFont.FreeTypeFont:
    """Try to get a decent font; fall back to default."""
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size=size)
    except OSError:
        try:
            return ImageFont.truetype("DejaVuSans.ttf", size=size)
        except OSError:
            try:
                return ImageFont.truetype("arial.ttf", size=size)
            except OSError:
                return ImageFont.load_default()
