FROM labhackercd/alpine-python3-nodejs

ENV BUILD_PACKAGES python3 python3-dev linux-headers curl curl-dev \
    git ca-certificates gcc postgresql-dev build-base bash \
    postgresql-client gettext libxml2-dev libxslt-dev zlib-dev jpeg-dev \
    libffi-dev

RUN apk add --update --no-cache $BUILD_PACKAGES

COPY Pipfile /var/labhacker/edemocracia/
COPY Pipfile.lock /var/labhacker/edemocracia/

COPY package.json /var/labhacker/edemocracia/
COPY package-lock.json /var/labhacker/edemocracia/

WORKDIR /var/labhacker/edemocracia

RUN pip install -U pipenv psycopg2 gunicorn
RUN pipenv install --system

RUN npm install && \
    npm rebuild node-sass --force

ADD . /var/labhacker/edemocracia

EXPOSE 8000
CMD ["python3", "src/manage.py", "runserver", "0.0.0.0:8000"]