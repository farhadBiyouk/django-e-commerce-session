FROM python:latest

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["qunicorn", "core:wsgi", ":8000"]