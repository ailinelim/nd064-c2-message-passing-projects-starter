FROM python:3.8.0

WORKDIR .

ENV GRPC_TRACE 'transport_security,tsi'
ENV GRPC_VERBOSITY 'DEBUG'

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5005

COPY . .

ENTRYPOINT [ "python", "app/grpc_host.py" ]