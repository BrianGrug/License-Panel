FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /panel
COPY requirements.txt /panel/
RUN pip install -r requirements.txt
COPY . /panel/