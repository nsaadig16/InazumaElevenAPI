FROM astral/uv:python3.12-alpine

WORKDIR /api

ADD uv.lock uv.lock
ADD pyproject.toml pyproject.toml
ADD .python-version .python-version

RUN uv sync

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uv run uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]