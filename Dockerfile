FROM continuumio/miniconda3

RUN mkdir /app 

# copy all source files to app folder
ADD . /app

# make app the current directory all 
# subsequent commands will be execute here

WORKDIR /app

# install the python dependencies

RUN conda install --file requirements.txt

ENTRYPOINT [ "python", "cli.py" ]