FROM arm32v6/python:3.7-alpine

RUN apk add --update alpine-sdk linux-headers

RUN export PIP_DEFAULT_TIMEOUT=100 && \
    pip3 install --upgrade pip && pip3 install --upgrade setuptools && \
    pip3 install ptvsd azure-iot-device psutil enviroplus RPi.GPIO
#RUN pip3 install sense-hat

# Add the application
ADD main.py .


ENV PYTHONUNBUFFERED=1

CMD ["python3","main.py"]

# export IOTHUB_DEVICE_CONNECTION_STRING=""
# docker run -d --privileged --restart always -e IOTHUB_DEVICE_CONNECTION_STRING=$IOTHUB_DEVICE_CONNECTION_STRING  --rm --name enviroplus  environment:latest
