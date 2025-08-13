ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}-slim-bookworm AS builder

WORKDIR /app

RUN python3 -m pip install build

COPY . .
RUN python3 -m build && \
    mkdir /wheels/ && \
    mv /app/dist/vibepython-*.whl /wheels/

FROM python:${PYTHON_VERSION}-slim-bookworm AS dependency

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache --no-cache-dir -r requirements.txt
COPY --from=builder /wheels /wheels
RUN pip install --no-cache --no-cache-dir /wheels/*

FROM gcr.io/distroless/python3-debian12
ARG PYTHON_VERSION=3.11

COPY --from=dependency /usr/local/lib/python${PYTHON_VERSION}/site-packages /usr/local/lib/python${PYTHON_VERSION}/site-packages

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONPATH=/usr/local/lib/python${PYTHON_VERSION}/site-packages

CMD [ "-m", "vibepython" ]
