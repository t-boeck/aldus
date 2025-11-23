FROM python:3.10-slim

# Install system dependencies including LaTeX
RUN apt-get update && apt-get install -y \
    texlive-xetex \
    texlive-lang-chinese \
    texlive-lang-spanish \
    texlive-lang-french \
    texlive-latex-recommended \
    texlive-latex-extra \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=aldus.app
ENV PORT=5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "300", "aldus.app:app"]
