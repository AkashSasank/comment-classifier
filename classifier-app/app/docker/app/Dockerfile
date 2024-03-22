FROM python:3.10
# Setting environment variables
ENV PYTHONUNBUFFERED 1

# Install requirements
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# Copy scripts and directories
COPY . /app
WORKDIR /app
CMD ["/app/runserver.sh"]