# Client-Accountant Invoice Management System

A secure web application for managing invoices between clients and accountants.

## Features

- Secure authentication for clients and accountants
- Invoice upload and management
- Dashboard views for both clients and accountants
- Expense and revenue tracking
- Document storage and retrieval
- Role-based access control

## Tech Stack

- Backend: Python/Django
- Frontend: React
- Database: PostgreSQL
- File Storage: AWS S3
- Authentication: JWT

## Project Structure

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

## Setup Instructions

1. Clone the repository
2. Set up environment variables
3. Install dependencies
4. Run migrations
5. Start the development servers

## Development

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## Environment Variables

Create a `.env` file in the backend directory with:

```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/fatture
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

## License

MIT 