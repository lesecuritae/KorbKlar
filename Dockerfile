FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends chromium ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install --no-cache-dir . \
    && useradd --system --uid 10001 --create-home --home-dir /home/korbklar korbklar \
    && mkdir -p /data \
    && chown -R korbklar:korbklar /data

USER korbklar
VOLUME ["/data"]
EXPOSE 8000

CMD ["uvicorn", "supermarkt.asgi:app", "--host", "0.0.0.0", "--port", "8000"]
