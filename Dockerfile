FROM python:3.6-stretch

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN pip install --upgrade pip

# Install requirements
ADD requirements.txt /code/
RUN pip install -r requirements.txt

# Install debugpy for python debugging in VS code
RUN pip install debugpy -t /tmp

ADD . /code/

CMD python3 manage.py runserver 0.0.0.0:$PORT
