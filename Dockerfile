FROM astral/uv:python3.12-alpine

WORKDIR /api

ADD uv.lock uv.lock
ADD pyproject.toml pyproject.toml
ADD .python-version .python-version

RUN uv sync

COPY . .

CMD [ "uvicorn", "/api/main:app", "-p", "8000", "--reload" ]