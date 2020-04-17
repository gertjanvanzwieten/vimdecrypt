FROM python:3.6

RUN apt-get update
RUN apt-get install -y build-essential libssl-dev libffi-dev python-dev

RUN mkdir /app
COPY ./ /app
WORKDIR /app

RUN pip3 install -r requirements.txt
RUN python setup.py install

ENTRYPOINT [ "python3", "vimdecrypt" ]