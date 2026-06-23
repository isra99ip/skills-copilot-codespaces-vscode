FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml README.md ./
COPY src ./src
COPY apps/dashboard ./apps/dashboard

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir ".[dashboard]"

EXPOSE 8501
CMD ["streamlit", "run", "apps/dashboard/app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]