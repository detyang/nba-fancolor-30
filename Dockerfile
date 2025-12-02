# Use Python 3.13 slim image
FROM python:3.13-slim

# Prevent .pyc and ensure unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system deps needed by Pillow etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy project metadata first (for layer caching)
COPY pyproject.toml uv.lock ./

# Install uv and sync dependencies (using 3.13)
RUN pip install --no-cache-dir uv \
 && uv sync --frozen --no-dev

# Make uv's virtualenv the default for all subsequent commands
ENV PATH="/app/.venv/bin:$PATH"

# Copy the rest of the project
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Run the Streamlit app; PORT is used by hosts like Railway/Fly
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0"]
