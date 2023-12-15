# Use an official Python runtime as a parent image
FROM osgeo/gdal:ubuntu-full-latest

# install python3 / pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# copy files
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r ./scripts/requirements.txt

# Define a volume for outputting data files
VOLUME /app

# Run your script when the container launches, with unbuffered output
CMD ["python3", "-u", "./scripts/clean_data.py"] 