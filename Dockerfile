FROM arm32v6/python:3.7-alpine

RUN apk add --update alpine-sdk linux-headers

COPY requirements.txt .

RUN export PIP_DEFAULT_TIMEOUT=100 && \
    pip3 install --upgrade pip && pip3 install --upgrade setuptools && \
    pip3 install -r requirements.txt


# Add the application
COPY *.py /

# Disable output buffering 
ENV PYTHONUNBUFFERED=1

CMD ["python3","main.py"]

# export IOTHUB_DEVICE_CONNECTION_STRING=""
# docker run -d --privileged --restart always -e IOTHUB_DEVICE_CONNECTION_STRING=$IOTHUB_DEVICE_CONNECTION_STRING  --rm --name enviroplus  environment:latest

# docker run -it --privileged -p 5678:5678 --rm  -v $PWD:/app   --name enviroplus --env-file envfile.env  environment:latest

# docker run -d --privileged -p 5678:5678 --rm  --name enviroplus --env-file envfile.env  environment:latest
