FROM ubuntu:18.04
RUN apt-get update
# Set the home directory to /root
ENV HOME /root
# cd into the home directory
WORKDIR /root
# Install Node
RUN apt-get update --fix-missing
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y mysql-client

COPY . .
EXPOSE 8600
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

RUN pip3 install django
RUN pip3 install -U channels
RUN pip3 install pymysql
RUN pip3 install pillow
RUN pip3 install django-mysql


CMD /wait && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8600
