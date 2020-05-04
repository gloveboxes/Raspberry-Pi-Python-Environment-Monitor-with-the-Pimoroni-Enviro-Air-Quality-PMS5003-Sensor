FROM arm32v6/python:3.7-alpine

RUN apk add --update alpine-sdk linux-headers

COPY requirements.txt .

RUN export PIP_DEFAULT_TIMEOUT=100 && \
    pip3 install --upgrade pip && pip3 install --upgrade setuptools && \
    pip3 install -r requirements.txt
#RUN pip3 install sense-hat

# Add the application
# ADD main.py .
# ADD device_provisioning_service.py .
# ADD sensor.py .

ENV PYTHONUNBUFFERED=1
RUN mkdir /app

CMD ["python3","/app/main.py"]

# export IOTHUB_DEVICE_CONNECTION_STRING=""
# docker run -d --privileged --restart always -e IOTHUB_DEVICE_CONNECTION_STRING=$IOTHUB_DEVICE_CONNECTION_STRING  --rm --name enviroplus  environment:latest

# docker run -it --privileged -p 5678:5678 --rm  -v $PWD:/app   --name enviroplus --env-file envfile.env  environment:latest
