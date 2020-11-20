FROM python:3
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN apt-get -y update
RUN pip3 install -r requirements.txt
EXPOSE 5001
CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:5001", "app_cardata:app"]
