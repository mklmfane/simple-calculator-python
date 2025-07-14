FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN rm -rf dist build src/*.egg-info && \
    python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt && \
    /opt/venv/bin/pip install build pytest && \
    /opt/venv/bin/python -m build && \
    /opt/venv/bin/pip install dist/*.whl && \
    /opt/venv/bin/pytest tests/

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 5000
