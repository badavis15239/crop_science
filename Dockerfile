# Use official Python image
FROM python:3.12.8

# Set the working directory inside the container
WORKDIR /app

# Copy the application code from the weather_api directory to the container
COPY weather_api/ /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]
