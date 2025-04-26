#!/bin/bash

# Create backend directory
mkdir -p backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install dependencies
pip install -r ../requirements.txt

# Create Django project
django-admin startproject config .

# Create apps
python manage.py startapp users
python manage.py startapp invoices
python manage.py startapp api

# Create necessary directories
mkdir -p media
mkdir -p static

# Create .env file
cat > .env << EOL
DEBUG=True
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DATABASE_URL=postgres://user:password@localhost:5432/fatture
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket-name
EOL

echo "Backend setup complete. Please update the .env file with your actual credentials." 