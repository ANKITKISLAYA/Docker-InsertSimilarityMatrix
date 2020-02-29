# FROM amd64/stefanscherer/python-windows:nano
FROM amd64/python:3.7.2-stretch

# FROM amd64/python:3.8.1-slim-buster

# Set the working directory to /app
WORKDIR /insertrecsys

# Copy the current directory contents into the container at /app 
ADD . /insertrecsys

# Install the dependencies
RUN pip install -r requirements.txt

# run the command to start uWSGI
CMD ["python", "app.py"]