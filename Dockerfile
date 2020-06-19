FROM python:3.8

WORKDIR /introdon

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pip install pipenv && \
    pipenv install --system

ENV PYTHONPATH /introdon

CMD ["./flask_env.sh"]
