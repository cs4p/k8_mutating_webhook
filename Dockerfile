FROM python:3.8

# switch working directory
WORKDIR /usr/src/app

# copy the requirements file into the image
COPY ./requirements.txt /usr/src/app/requirements.txt

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY app.py /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]