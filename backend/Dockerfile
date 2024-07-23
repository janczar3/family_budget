FROM python:3.11-slim-bullseye
WORKDIR /srv/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY ./requirements.txt .

#RUN apt-get update && apt-get install -y \
#  gcc \
#  netcat \
#  libpq-dev \
#  && apt-get clean

RUN pip install -r requirements.txt

COPY ./entrypoint.sh .

COPY . .

ENTRYPOINT ["/srv/app/entrypoint.sh"]