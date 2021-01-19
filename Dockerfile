FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /panel

RUN pip install --upgrade pip

RUN pip install django

COPY requirements.txt /panel/
RUN pip install -r requirements.txt
EXPOSE 8001

COPY . /panel/

RUN chmod u+rwx manage.py

RUN ./manage.py makemigrations
RUN ./manage.py migrate

CMD python3 manage.py runserver 0.0.0.0:8001