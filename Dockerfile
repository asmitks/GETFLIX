FROM ubuntu:16.04
MAINTAINER asmitks "asmitsingh89@gmail.com"
RUN apt-get update -y && apt-get install -y python3-dev python3-pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

#RUN apt-get -y install python3-pip
RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
