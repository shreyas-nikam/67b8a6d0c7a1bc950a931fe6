# Use an official Python image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install virtualenv & create a virtual environment inside the container
RUN python -m venv venv &&     ./venv/bin/pip install --no-cache-dir --upgrade pip &&     ./venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose Streamlit's default port (can be overridden in Docker Compose)
EXPOSE 8501

# Run the application inside the virtual environment
CMD ["bash", "-c", "source venv/bin/activate && streamlit run app.py --server.port=8501 --server.headless=true"]
