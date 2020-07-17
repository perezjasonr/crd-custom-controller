FROM python:3.8-slim-buster AS base
ENV PYTHONUSERBASE /basedir
# pipenv will make this if it doesnt exist

FROM base AS builder
WORKDIR /app
RUN pip3 install pipenv
# other pip args: --user --ignore-installed, user would put in userbase?
COPY Pipfile Pipfile.lock /app/
ENV PIP_USER 1
ENV PIP_IGNORE_INSTALLED 1
# ENVS come after pip call or they screw up pipenv location
RUN pipenv install --system  --deploy --ignore-pipfile

FROM base AS final
WORKDIR /app
COPY --from=builder $PYTHONUSERBASE/lib/ $PYTHONUSERBASE/lib/
# python -m site --user-base/--user-site
# note flask is in --user-base bin
COPY app/custom_controller.py /app/
ENTRYPOINT ["python", "custom_controller.py"]