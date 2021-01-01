FROM python:3.9.0-slim-buster

RUN mkdir /usr/src/app 
WORKDIR /usr/src/app

COPY build/requirements.txt ./
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY build/ .

CMD [ "python", "-m", "daemon" ]