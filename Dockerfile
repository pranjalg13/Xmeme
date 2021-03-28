FROM python:3

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /xmeme

# Set the working directory to /xmeme
WORKDIR /xmeme

# Copy the current directory contents into the container at /xmeme
ADD . /xmeme/

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt
