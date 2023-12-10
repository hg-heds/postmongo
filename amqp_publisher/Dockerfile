FROM python 
COPY . /app
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir psycopg2 && \
    pip install --no-cache-dir pika
WORKDIR /app
CMD python postmongo_pika_publisher.py