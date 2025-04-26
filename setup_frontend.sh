#!/bin/bash

# Create frontend directory
mkdir -p frontend
cd frontend

# Create React app
npx create-react-app .

# Install additional dependencies
npm install @mui/material @emotion/react @emotion/styled
npm install @mui/icons-material
npm install axios
npm install react-router-dom
npm install @reduxjs/toolkit react-redux
npm install formik yup
npm install date-fns
npm install chart.js react-chartjs-2

# Create directory structure
mkdir -p src/components
mkdir -p src/pages
mkdir -p src/services
mkdir -p src/store
mkdir -p src/utils
mkdir -p src/hooks
mkdir -p src/assets

# Create .env file
cat > .env << EOL
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_WS_URL=ws://localhost:8000/ws
EOL

echo "Frontend setup complete. Please update the .env file with your actual API URLs." 