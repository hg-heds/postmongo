FROM python 
COPY . /app
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pymongo && \
    pip install --no-cache-dir pika
WORKDIR /app
CMD python postmongo_pika_consumer.py