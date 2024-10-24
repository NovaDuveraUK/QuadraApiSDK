# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /var/task



# Copy the Python requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY src/ src/
COPY scripts/ scripts/

ENV PYTHONPATH=/var/task

# Expose port (if necessary for other services, Telegram bot doesn't need this)
# EXPOSE 8000

# Set environment variables (optional, you can also use a .env file in production)
# ENV TELEGRAM_BOT_TOKEN=<Your-Token-Here>

# Run the bot when the container launches
CMD ["python", "scripts/app.py"]
