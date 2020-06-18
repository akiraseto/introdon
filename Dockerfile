FROM python:3.8

WORKDIR /introdon
COPY . /introdon
COPY cmd.sh /

RUN pip install pipenv

COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install --system

ENV PYTHONPATH /introdon

CMD ["/cmd.sh"]
