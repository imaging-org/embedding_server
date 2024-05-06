FROM python as compiler
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y && apt-get dist-upgrade -y

WORKDIR /app/

RUN python -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -Ur requirements.txt

FROM python:3.12.3-alpine3.19 as runner
WORKDIR /app/
COPY --from=compiler /opt/venv /opt/venv

# Enable venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . /app/
EXPOSE 5545
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
