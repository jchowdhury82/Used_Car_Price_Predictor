FROM python:3
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN apt-get -y update
RUN pip3 install -r requirements.txt
EXPOSE 5000
RUN chmod +x ./entry.sh
ENTRYPOINT ["sh", "entry.sh"]