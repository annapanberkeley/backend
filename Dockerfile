FROM python:3.7-alpine
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 5000

CMD ["python", "app.py"]

# when do we use this version of Dockerfile?
# FROM python:3
# COPY . /app
# WORKDIR /app
# RUN pip install -r requirements.txt
# EXPOSE 5000
# ENTRYPOINT ["flask"]
# CMD ["run", "--host=0.0.0.0"]