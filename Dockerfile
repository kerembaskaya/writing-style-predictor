FROM python:3.9-slim-bullseye as base

RUN apt-get update -y && \
    apt-get install -y \
       libblas-dev \
       liblapack-dev \
       libpng-dev \
       locales \
       libssl-dev \
       libffi-dev \
       libfreetype6-dev

RUN mkdir -p /build/tests
RUN mkdir /applications

COPY requirements.txt /build/requirements.txt
RUN pip3 install -r /build/requirements.txt

#RUN pip3 install \ #  --no-color --progress-bar off \
    #-r /build/requirements.txt \
    #-r /build/requirements-test.txt # | ts -i '%.S'

COPY requirements-test.txt /build/requirements-test.txt
RUN pip3 install -r /build/requirements-test.txt

COPY .isort.cfg /build/.isort.cfg
COPY pytest.ini /build/pytest.ini
COPY .flake8 /build/.flake8

COPY style /build/style
COPY tests /build/tests
COPY resources /applications/resources
COPY datasets /applications/datasets
COPY models /applications/models

ENV APP_RESOURCE_DIR /applications

ARG skip_tests

RUN \
    if [ "$skip_tests" = "" ] ; then \
        black \
           -t py39 -l 80 \
           --check $(find /build/style /build/tests -name "*.py") \
      && \
        # isort --df --settings-path=/build/.isort.cfg --check /build/style \
      #&& \
        flake8 --config=/build/.flake8 /build/style \
      && \
        pytest /build/tests ; \
      else \
        echo "Skipping tests" ; \
    fi

FROM base as style_app

COPY --from=base /build/style /applications/style

ENV PYTHONPATH /applications

ENTRYPOINT ["python3", "applications/style-app-entrypoint.sh"]
