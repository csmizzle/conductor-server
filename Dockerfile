FROM python:3.12.3
RUN apt-get update && apt-get install -y \
    git gcc python3-dev

WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip cache purge && pip install --no-cache-dir -r requirements.txt

COPY ./conductor_server ./conductor_server
COPY ./agents ./agents
COPY ./search ./search
COPY ./users ./users
COPY ./manage.py ./manage.py
COPY ./start.sh ./start.sh

RUN python manage.py collectstatic --noinput

CMD [ "sh", "./start.sh" ]
