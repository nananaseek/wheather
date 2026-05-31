FROM ubuntu:latest
LABEL authors="mef"

FROM python:3.13.3-bookworm

WORKDIR /Weather

COPY pyproject.toml /Weather/
COPY README.md /Weather/

RUN pip install --no-cache-dir uv
RUN uv sync --no-dev

COPY . .

# CMD ["sh", "-c", "uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
