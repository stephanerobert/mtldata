FROM python:3.7

ENV APP_EXPOSED_PORT 8000
ENV HTTP_TIMEOUT 300
ENV APP_ROOT /opt/hakilogix

RUN mkdir $APP_ROOT && \
    mkdir /etc/mtldata && \
    chown -R nobody:nogroup /etc/mtldata

COPY requirements.txt setup.py setup.cfg MANIFEST.in docker-files/hypercorn.toml $APP_ROOT/

WORKDIR $APP_ROOT

RUN git init && \
    pip install -r requirements.txt

COPY mtldata $APP_ROOT/mtldata
COPY deploy/config $APP_ROOT/mtldata/resources/config
RUN python setup.py install

EXPOSE $APP_EXPOSED_PORT
USER nobody

HEALTHCHECK --interval=5s --timeout=3s CMD curl --fail http://localhost:$APP_EXPOSED_PORT/healthcheck

CMD hypercorn mtldata.main:app -c hypercorn.toml
