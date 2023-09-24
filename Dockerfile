FROM python:3.10 AS compile-image

## install dependencies

RUN apt-get update && \
    apt-get install -y --no-install-recommends

## add and install requirements
COPY req.txt .
RUN pip install --upgrade pip &&  \
    pip install --no-cache-dir -r req.txt


FROM python:3.10 AS build-image

# copy env from prev img
COPY --from=compile-image /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

COPY . /app

WORKDIR /app

CMD ["sh", "-c" ,"python3 -m alembic upgrade head && python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]