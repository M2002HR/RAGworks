# Minimal image for the Gradio demos (multi-service via APP_PATH)
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_INDEX_URL=https://pypi.org/simple \
    GRADIO_SERVER_NAME=0.0.0.0 \
    GRADIO_SERVER_PORT=7860 \
    OPENAI_API_KEY=PLACEHOLDER
ENV APP_PATH=app/demo_gradio.py

WORKDIR /app

# Install Python deps first for better layer caching
COPY requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir --prefer-binary --retries 10 -r requirements.txt --index-url https://pypi.org/simple

# Copy source and install the package (src/ layout)
COPY . /app
RUN pip install -e .

EXPOSE 7860
CMD ["sh", "-c", "python ${APP_PATH}"]
