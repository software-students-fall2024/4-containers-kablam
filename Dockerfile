FROM python:3.10-slim
# Set the working directory within the image to /app
WORKDIR /app
# Copy the current directory contents into the container at /app
COPY src /app/src
COPY web_app /app/web_app
# Install any needed packages specified in requirements.txt
# in Python, a requirements.txt file is a way of indicating dependencies in a way that the package manager, pip, can understand
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt
# by default Docker containers are closed off to the external world
# Make port 80 available to the world outside this container
EXPOSE 5000
# Define an environment variable... this will be available to programs running inside the container
ENV PYTHONPATH="/app/src:$PYTHONPATH"
# Run app.py when the container launches
CMD ["python3", "web_app/app.py"]