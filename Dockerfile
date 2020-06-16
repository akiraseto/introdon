FROM python:3.8

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi

WORKDIR /introdon
COPY . /introdon
COPY cmd.sh /

RUN pip install pipenv

COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install --system

ENV PYTHONPATH /introdon

USER uwsgi

CMD ["/cmd.sh"]
