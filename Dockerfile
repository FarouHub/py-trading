FROM python:alpine3.17

# install dependencies
COPY ./requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt


CMD ["python", "./main"]