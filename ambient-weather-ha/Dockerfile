# Stage 1: Build and Test
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

WORKDIR /app

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# Copy source code and tests
COPY app/ app/
COPY tests/ tests/

# Set environment variables for tests
ENV HOME_ASSISTANT_URL=http://mock-ha
ENV HOME_ASSISTANT_TOKEN=mock-token
ENV AMBIENT_WEATHER_PASSKEY=test_passkey

# Run tests
RUN uv run pytest

# Stage 2: Production
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install uv for the final stage or just copy the venv
COPY --from=builder /app/.venv /app/.venv
COPY app/ app/

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Expose the port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
