# 📊 Client-Accountant Invoice Management System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.0.2-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18.0-blue.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-🐳-blue.svg)](https://www.docker.com/)

A modern, secure web application for managing invoices between clients and accountants. Built with Django and React. 🚀

## ✨ Features

- 🔐 Secure authentication for clients and accountants
- 📄 Invoice upload and management
- 📊 Interactive dashboard views
- 💰 Expense and revenue tracking
- 🗄️ Document storage and retrieval
- 👥 Role-based access control

## 🛠️ Tech Stack

- 🐍 **Backend**: Python/Django
- ⚛️ **Frontend**: React
- 🐘 **Database**: PostgreSQL
- ☁️ **File Storage**: AWS S3
- 🔑 **Authentication**: JWT

## 📁 Project Structure

```
fatture/
├── backend/           # Django backend
│   ├── api/          # REST API endpoints
│   ├── core/         # Core functionality
│   └── users/        # User management
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── public/
└── docker/           # Docker configuration
```

## 🚀 Setup Instructions

1. 📥 Clone the repository
2. ⚙️ Set up environment variables
3. 📦 Install dependencies
4. 🔄 Run migrations
5. 🎯 Start the development servers

### 🐍 Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### ⚛️ Frontend Setup

```bash
cd frontend
npm install
npm start
```

## 🔧 Environment Variables

Create a `.env` file in the backend directory with:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/fatture
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

## 🐳 Docker Support

The application can be run using Docker Compose:

```bash
docker-compose up --build
```

This will start:
- 🐘 PostgreSQL database
- 🐍 Django backend
- ⚛️ React frontend

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Material-UI for the beautiful React components
- Django REST framework for the powerful API tools
- All our contributors and users 