FROM amancevice/pandas:1.1.2-alpine

RUN mkdir /app 

# copy all source files to app folder
ADD . /app

# make app the current directory all 
# subsequent commands will be execute here

WORKDIR /app

# pip upgrade required
RUN pip install --upgrade pip

# install the python dependencies

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "cli.py" ]