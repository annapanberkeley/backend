FROM python:3.7-alpine

# Copy relevant files to container
COPY ./sender.py /app/
COPY ./requirements.txt /app/
COPY ./mailgun_config.json /app/

WORKDIR /app

# Install requirements
RUN pip3 install -r requirements.txt
EXPOSE 5000

# Start worker
# ENTRYPOINT ["rq"]
# CMD ["worker", "--with-scheduler", "--url", "redis://redis-container:6379"]