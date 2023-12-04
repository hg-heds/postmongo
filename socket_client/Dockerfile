FROM python 
COPY . /app
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir psycopg2
WORKDIR /app
CMD python postmongo_socket_client.py