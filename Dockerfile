FROM python:3.10-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY ./API/. /app/

RUN apt-get update && apt-get -y install build-essential cmake protobuf-compiler

RUN pip install dlib

RUN pip3 install --upgrade pip
RUN pip3 install gunicorn
RUN pip3 install --upgrade -r /app/requirements.txt



# ADD ./templates /app/templates
# ADD ./static /app/static
# ADD ./.env /app/
# ADD ./docker /app/docker 


EXPOSE 8000
#RUN chmod a+x /app/docker/backend/wsgi-entrypoint.sh
#RUN ["chmod", "a+x", "/app/docker/backend/wsgi-entrypoint.sh"]
#CMD ["/app/docker/backend/wsgi-entrypoint.sh"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app:app", "--bind", "0.0.0.0:8000"] 