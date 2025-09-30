# Minimal image for the Gradio demo
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    GRADIO_SERVER_PORT=7860 \
    OPENAI_API_KEY=PLACEHOLDER

WORKDIR /app

# Install Python deps
COPY requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

# Copy repo and install the package (src/ layout)
COPY . /app
RUN pip install -e .

EXPOSE 7860
CMD ["python", "app/demo_gradio.py"]
