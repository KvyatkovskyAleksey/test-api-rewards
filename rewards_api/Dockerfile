# IMAGE: dfscrunch/api-base:master
FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install required packages: Python, pip and curl
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Prepare app specific modules
COPY ["pyproject.toml", "./"]
COPY ["uv.lock", "./"]

# Install Python packages
RUN pip3 install --upgrade pip && \
    pip3 install uv && \
    uv pip install . --system

ONBUILD COPY ./rewards_api /app
ONBUILD RUN chown -R app:app /app
ONBUILD USER app