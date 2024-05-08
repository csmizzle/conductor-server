FROM python:3.12.3-slim-bullseye
RUN apt-get update && apt-get install -y git

WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./conductor_server ./conductor_server
COPY ./agents ./agents
COPY ./search ./search
COPY ./users ./users
COPY ./manage.py ./manage.py

RUN python manage.py collectstatic --noinput

CMD [ "sh", "start.sh" ]
