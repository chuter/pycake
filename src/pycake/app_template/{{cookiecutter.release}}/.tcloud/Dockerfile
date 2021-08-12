
FROM harbor.weizhipin.com/tcloud/python:xgboost-01

COPY .release/ /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 9502
CMD python ./app.py
