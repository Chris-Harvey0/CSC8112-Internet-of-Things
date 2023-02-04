# Base on image_full_name (e.g., ubuntu:18.04) docker image
FROM python:3.8.12

# Switch to root
USER root

# Copy all sources files to workdir
ADD data_subscriber.py /usr/local/source/
ADD data_processor.py /usr/local/source/
ADD requirements.txt /usr/local/source/

# Change working dir
WORKDIR /usr/local/source

# Prepare project required running system environments
# requirements.txt is a document that pre-define any
# python dependencies with versions required of your code
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Start task
CMD python3 data_subscriber.py
