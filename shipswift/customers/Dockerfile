# start by pulling the python image
FROM python:3.8-alpine

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# create a temporary directory in /app and copy 'DB' into it
# copy everything else from the local file to the image
COPY . /app

# expose the port
EXPOSE 5000

# specify the command to run on container start
CMD ["python3", "app.py"]