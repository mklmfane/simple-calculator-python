# ==========================
# STAGE 1: Build & test
# ==========================
FROM python:3.13-slim AS builder

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

# ==========================
# STAGE: SAST analysis with Bandit
# ==========================
FROM python:3.13-slim AS sast
WORKDIR /scan

# Copy your source code into /scan
COPY . /scan

# Setup Python and install Bandit
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install bandit

# Run Bandit scan recursively, output to JSON and text
RUN /opt/venv/bin/bandit -r /scan -f json -o /scan/bandit-report.json --exit-zero && \
    /opt/venv/bin/bandit -r /scan -f txt -o /scan/bandit-report.txt --exit-zero

# For convenience, make the default container CMD show the report
CMD ["cat", "/scan/bandit-report.txt"]

# ==========================
# STAGE 3: Final runtime
# ==========================
FROM python:3.13-slim AS final

WORKDIR /app
COPY --from=builder /app /app

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt && \
    /opt/venv/bin/pip install dist/*.whl

ENV PATH="/opt/venv/bin:$PATH"
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "127.0.0.1:5000", "simple_calculator.main:app"]
