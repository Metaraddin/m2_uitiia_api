FROM python
ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip && \
  pip install --upgrade setuptools

WORKDIR /api

COPY requirements.txt /api/requirements.txt
RUN pip install -r /api/requirements.txt
COPY ./ /api

CMD /api/run.sh