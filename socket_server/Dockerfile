FROM python 
COPY . /app
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pymongo
WORKDIR /app
CMD python postmongo_socket_server.py