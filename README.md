---
title: NBA Fan Color 30
emoji: 🏀
colorFrom: blue
colorTo: red
sdk: docker
app_file: Dockerfile
pinned: false
---

# NBA Fan Color 30 🎨🏀

A Streamlit-based web app that lets users color their NBA team fan ratings and export a shareable poster.

## Features
- Interactive 30-team canvas
- Custom color palette (Hometeam → Hate)
- Freehand drawing on each team circle
- Save full poster (title + palette + canvas)
- Shareable on social media
- Clean CSS-styled UI

## Tech Stack
- Python
- Streamlit
- streamlit-drawable-canvas
- Pillow
- uv package manager

## Run locally

```bash
uv sync
streamlit run app.py
```
