FROM python:3.12.9-slim-bullseye AS base
RUN groupadd -g 30000 -r app \
    && useradd -u 30000 -r -g app -s /usr/sbin/nologin app \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    curl=7.*
WORKDIR /home/app
RUN chown -R app:app /home/app
USER app

FROM base AS poetry
ENV PATH="/home/app/.local/bin:${PATH}" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VERSION=2.0.1
RUN curl -sSL https://install.python-poetry.org | python3 -
COPY --chown=app:app pyproject.toml poetry.lock ./


FROM poetry AS dev-build
USER root
RUN apt-get update && apt-get install -y gcc=* python3-dev=* --no-install-recommends
USER app
RUN poetry install -v --no-root


FROM base AS runtime
ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=off \
    VIRTUAL_ENV="/home/app/.venv" \
    PATH="/home/app/.venv/bin:${PATH}"
COPY --chown=app:app src/ src/
COPY --chown=app:app migrations/ migrations/


FROM runtime AS dev
COPY --chown=app:app --from=dev-build /home/app/.venv /home/app/.venv/
COPY --chown=app:app tests/ tests/
COPY --chown=app:app pyproject.toml alembic.ini ./
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "--reload", "src.main:app"]
