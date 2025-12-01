# nba_fancolor_30/ui_main.py

from pathlib import Path
import io

import streamlit as st
from streamlit_drawable_canvas import st_canvas

from PIL import Image, ImageDraw, ImageFont

from .data import TEAMS, NUM_COLS, COLOR_MAP
from .canvas_template import build_base_template


def _render_color_palette() -> None:

    options = list(COLOR_MAP.keys())

    # One-time initialization of radio + brush state
    if "brush_radio" not in st.session_state:
        st.session_state["brush_radio"] = "Neutral"

    current = st.session_state["brush_radio"]

    # Use the current radio value to set the index
    try:
        default_index = options.index(current)
    except ValueError:
        default_index = options.index("Neutral")

    choice = st.radio(
        label="Select Brush Color",
        options=options,
        index=default_index,
        horizontal=True,
        width=900,
        label_visibility="hidden",
    )

    st.session_state["brush_label"] = choice
    st.session_state["brush_color"] = COLOR_MAP[choice]

def build_palette_strip(color_map: dict[str, str], width: int, height: int = 70) -> Image.Image:
    img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except OSError:
        font = ImageFont.load_default()

    items = list(color_map.items())
    n = len(items)
    block_w = width // n

    for i, (label, hex_color) in enumerate(items):
        x0 = i * block_w
        x1 = x0 + block_w

        draw.rectangle([x0, 0, x1, height], fill=hex_color)

        # NEW: use textbbox
        bbox = draw.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

        # Neutral/dislike have dark text instead of white
        text_color = "#111827" if label in ("Neutral", "Dislike") else "#ffffff"

        draw.text(
            (x0 + block_w/2 - tw/2, height/2 - th/2),
            label,
            fill=text_color,
            font=font,
        )

    return img

def build_title_bar(text: str, width: int, height: int = 80) -> Image.Image:
    img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except OSError:
        font = ImageFont.load_default()

    # NEW: use textbbox instead of textsize
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    draw.text(
        ((width - tw) / 2, (height - th) / 2),
        text,
        fill="#111827",
        font=font,
    )
    return img

def load_css():
    css_path = Path(__file__).parent / "assets" / "styles.css"
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_app() -> None:
    st.set_page_config(page_title="NBA Fan Color 30", layout="centered")

    load_css()

    st.title("🏀 NBA Fan Color 30  ")
    st.markdown('<p class="subtitle">DIY your own NBA fan color poster.</p>', unsafe_allow_html=True)

    # Build base template
    if "base_template" not in st.session_state:
        base_img = build_base_template()
        st.session_state["base_template"] = base_img
    else:
        base_img = st.session_state["base_template"]

    # Ensure background for canvas is RGB (not RGBA)
    canvas_bg = base_img.convert("RGB")
    
    # ----- Palette at top -----
    _render_color_palette()

    # Get current brush color (from COLOR_MAP)
    brush_color = st.session_state.get("brush_color", COLOR_MAP["Neutral"])

    st.markdown(
        """
        - Use your mouse or trackpad to draw.
        - Change the color using the palette above.
        """
    )

    # --- Canvas (bottom) ---
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",
        stroke_width=20,
        stroke_color=brush_color,
        background_color="#ffffff",
        background_image=canvas_bg, 
        height=canvas_bg.height,
        width=canvas_bg.width,
        drawing_mode="freedraw",
        display_toolbar=False,
        key="team_canvas",
    )

    final_canvas = None  # will hold base + drawing

    if canvas_result is not None and canvas_result.image_data is not None:
        # User drawing layer (transparent)
        overlay = Image.fromarray(
            canvas_result.image_data.astype("uint8"),
            mode="RGBA",
        )

        # Start from base template
        base_rgba = base_img.convert("RGBA").copy()

        # Make sure overlay matches base size (just in case)
        if overlay.size != base_rgba.size:
            overlay = overlay.resize(base_rgba.size)

        # Composite drawing on top of base template
        base_rgba.alpha_composite(overlay)

        final_canvas = base_rgba
    
    poster_bytes = None

    if final_canvas is not None:
        width = final_canvas.width

        title_bar = build_title_bar("NBA Fan Color 30", width)
        palette_bar = build_palette_strip(COLOR_MAP, width)

        total_height = title_bar.height + palette_bar.height + final_canvas.height

        poster = Image.new("RGBA", (width, total_height), (255, 255, 255, 255))

        y = 0
        poster.paste(title_bar, (0, y))
        y += title_bar.height

        poster.paste(palette_bar, (0, y))
        y += palette_bar.height

        poster.paste(final_canvas, (0, y))

        buf = io.BytesIO()
        poster.save(buf, format="PNG")
        poster_bytes = buf.getvalue()

    st.markdown("### Export")

    col_save, col_share = st.columns(2)

    with col_save:
        if poster_bytes is not None:
            st.download_button(
                "💾 Save image",
                data=poster_bytes,
                file_name="nba_fancolor_30.png",
                mime="image/png",
            )
        else:
            st.caption("Draw something on the canvas to enable saving.")

    with col_share:
        if poster_bytes is not None:
            if st.button("📤 Share"):
                st.info(
                    "1. Click **Save image** to download your poster.\n"
                    "2. Upload the PNG to your favorite platform (X, TikTok, Reddit, etc.).\n\n"
                    "Quick link for X: "
                    "[Compose a post](https://twitter.com/intent/tweet?text=My%20NBA%20Fan%20Color%2030%20poster%20%F0%9F%8F%80%20%23NBA%20%23FanColor30)"
                )
        else:
            st.caption("Create your poster first, then you can share it.")