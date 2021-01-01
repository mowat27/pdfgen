FROM python:3.9.0-slim-buster

RUN apt-get update && apt-get install -y \
  wkhtmltopdf \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /usr/src/app 
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-m", "generator.daemon" ]