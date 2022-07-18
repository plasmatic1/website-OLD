FROM python:3.9.2

# Args
ARG DJANGO_SUPERUSER_USERNAME
ARG DJANGO_SUPERUSER_EMAIL
ARG DJANGO_SUPERUSER_PASSWORD

# Copy files
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .

# Do installation
RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic
RUN python manage.py noinput_createsuperuser $DJANGO_SUPERUSER_USERNAME $DJANGO_SUPERUSER_EMAIL $DJANGO_SUPERUSER_PASSWORD

# Running
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "website.wsgi"]