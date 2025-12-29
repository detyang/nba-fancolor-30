<!--
NOTE:
The following YAML front-matter is REQUIRED by Hugging Face Spaces
to configure and deploy this application (Docker SDK, app entry, UI metadata).
Do not remove unless you also update the Hugging Face Space configuration.
-->

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


## Tech Stack
- Python
- Streamlit
- streamlit-drawable-canvas
- Pillow
- uv package manager
- Docker
- HuggingFace Space


## Run locally

```bash
uv sync
streamlit run app.py
```
