FROM python:3.8 as stage1

# switch working directory
WORKDIR /usr/src/app

RUN apt update -y && apt install -y apache2-dev

# copy the requirements file into the image
COPY ./requirements.txt ./requirements.txt

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

COPY wsgi.py wsgi.py
COPY flaskr ./flaskr

# Create Service account
RUN useradd -u 1001 flask
RUN chmod -R o+r .


FROM stage1

USER 1001

CMD ["mod_wsgi-express", "start-server", "wsgi.py", "--processes", "4"]