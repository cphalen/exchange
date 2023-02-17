FROM python:3.10.7-slim-buster

WORKDIR /app

# install poetry
RUN pip install poetry

COPY pyproject.toml poetry.lock ./

# install python dependencies
RUN poetry install

# copy application source code
COPY . .

# start the server with parameters specified in environment variables
CMD ["poetry", "run", "python", "-m", "server.server"]
