# nba_fancolor_30/ui_main.py

from pathlib import Path
import io

import streamlit as st
from streamlit_drawable_canvas import st_canvas

from PIL import Image, ImageDraw, ImageFont

from .data import TEAMS, NUM_COLS, COLOR_MAP
from .canvas_template import build_base_template


def _get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Prefer a packaged font that exists on Linux (HF) over platform fonts."""
    faces = [
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "arial.ttf",
    ]

    for name in faces:
        try:
            return ImageFont.truetype(name, size=size)
        except OSError:
            continue

    return ImageFont.load_default()


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

def build_palette_strip(color_map: dict[str, str], width: int, height: int = 80) -> Image.Image:
    img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    font = _get_font(26, bold=True)

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

def build_title_bar(text: str, width: int, height: int = 90) -> Image.Image:
    img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    font = _get_font(48, bold=True)

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

    col_save, col_share = st.columns(2, gap="small")

    with col_save:
        if poster_bytes is not None:
            st.download_button(
                "Save image",
                data=poster_bytes,
                file_name="nba_fancolor_30.png",
                mime="image/png",
                use_container_width=True,
            )
        else:
            st.caption("Draw something on the canvas to enable saving.")

    with col_share:
        if poster_bytes is not None:
            if st.button("Share", use_container_width=True):
                st.info(
                    "1. Click **Save image** to download your poster.\n"
                    "2. Upload the PNG to your favorite platform (X, TikTok, Reddit, etc.).\n\n"
                    "Quick link for X: "
                    "[Compose a post](https://twitter.com/intent/tweet?text=My%20NBA%20Fan%20Color%2030%20poster%20%F0%9F%8F%80%20%23NBA%20%23FanColor30)"
                )
        else:
            st.caption("Create your poster first, then you can share it.")

    st.markdown(
        """
        <div class="footer">
            Developed by
            <a class="footer-link" href="https://github.com/detyang" target="_blank" rel="noopener">
                <svg class="footer-icon" viewBox="0 0 16 16" aria-hidden="true">
                    <path d="M8 0C3.58 0 0 3.66 0 8.18c0 3.62 2.29 6.68 5.47 7.76.4.08.55-.18.55-.39 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.5-2.69-.96-.09-.24-.48-.96-.82-1.15-.28-.15-.68-.52-.01-.53.63-.01 1.08.6 1.23.85.72 1.23 1.87.88 2.33.67.07-.53.28-.88.51-1.08-1.78-.2-3.64-.91-3.64-4.05 0-.9.31-1.64.82-2.22-.08-.2-.36-1.02.08-2.12 0 0 .67-.22 2.2.85.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.08 2.2-.85 2.2-.85.44 1.1.16 1.92.08 2.12.51.58.82 1.32.82 2.22 0 3.15-1.87 3.84-3.65 4.05.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.19 0 .21.15.46.55.39A8.09 8.09 0 0 0 16 8.18C16 3.66 12.42 0 8 0Z"></path>
                </svg>
                Det Yang
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )
