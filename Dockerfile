FROM python:3-alpine3.8

RUN mkdir /app 

# copy all source files to app folder
ADD . /app

# make app the current directory all 
# subsequent commands will be execute here

WORKDIR /app

# install the python dependencies

RUN pip -r requirements.txt

ENTRYPOINT [ "python", "cli.py" ]