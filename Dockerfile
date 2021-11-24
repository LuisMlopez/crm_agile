FROM python:3.6-stretch

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN pip install --upgrade pip

# Install requirements
ADD requirements.txt /code/
#ADD requirements-local.txt /code/
RUN pip install -r requirements.txt
#RUN pip install -r requirements-local.txt

# Install debugpy for python debugging in VS code
RUN pip install debugpy -t /tmp

ADD . /code/
