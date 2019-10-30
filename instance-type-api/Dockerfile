# select the base image
FROM python:3.6.3-alpine3.7

# copy the current directory to /app
COPY . /app

# set the correct work directory
WORKDIR /app

# install the dependencies
RUN pip install -r requirements.txt

# run the server
CMD ["./runserver.sh"]