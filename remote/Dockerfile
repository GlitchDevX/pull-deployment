FROM ghcr.io/astral-sh/uv:alpine

RUN apk add --no-cache git

COPY pyproject.toml uv.lock ./

# Disable development dependencies
ENV UV_NO_DEV=1

RUN uv sync --locked

COPY . .

CMD ["uv", "run", "fastapi", "run", "main.py", "--port", "8080"]
