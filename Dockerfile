# Use the official Python 3.13 slim image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all the contents of the current context (which is already ./backend)
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port your Django app runs on
EXPOSE 8000

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Default command to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]