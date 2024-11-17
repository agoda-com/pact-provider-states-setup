FROM python:3.13.0-alpine3.20
COPY server.py /opt/pact-provider-states-setup/server.py
EXPOSE 8000
ENV PROVIDER_BASE_URL="http://localhost/"
ENTRYPOINT ["python", "/opt/pact-provider-states-setup/server.py"]
