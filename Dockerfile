#set base image
FROM python:3.8

#set working directory
WORKDIR /app

# COPY requirements.txt /
COPY . /app

# install dependencies
RUN pip3 install -r requirements.txt


# command to run on container start
CMD [ "python3", "talos.py" ]