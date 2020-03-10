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

COPY . .

RUN pip3 install django

EXPOSE 8000

CMD ["python3", "helloworld.py"]