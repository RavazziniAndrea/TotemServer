FROM python:3.11.1-slim

# set work directory
WORKDIR /app
COPY ./app /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN pip install fastapi; pip install uvicorn
RUN pip install -r requirements.txt
RUN apt update && apt -y install libpq-dev gcc && pip install psycopg2
# RUN pip install psycopg2 && python setup.py build && python setup.py install

#CMD [ "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0" ]
CMD ["python3", "app/server.py"]