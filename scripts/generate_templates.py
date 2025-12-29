# scripts/generate_templates.py

from __future__ import annotations

from pathlib import Path
import sys

# Ensure repo root is on sys.path so `import nba_fancolor_30...` works when run as a script
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
from nba_fancolor_30.canvas_template import build_base_template

OUT = Path("nba_fancolor_30/assets/templates")
OUT.mkdir(parents=True, exist_ok=True)

for size in (75, 95, 115):
    img = build_base_template(cell_size=size)
    img.save(OUT / f"base_{size}.png")
    print("saved", OUT / f"base_{size}.png")