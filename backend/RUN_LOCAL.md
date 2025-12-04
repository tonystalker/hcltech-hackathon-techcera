# Running the Server Locally

## Quick Start

### Option 1: Using Python directly
```bash
cd backend
python main.py
```

### Option 2: Using uvicorn
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: Using the batch file (Windows)
Double-click `start.bat` in the backend folder

## Prerequisites

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up MongoDB:**
   - Install MongoDB locally, OR
   - Use MongoDB Atlas (cloud)
   - Create a `.env` file in the `backend` directory:
     ```
     MONGODB_URI=mongodb://localhost:27017
     DATABASE_NAME=healthcare_portal
     SECRET_KEY=your-secret-key-here
     ```

## Verification

Once the server starts, you should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Test the server:

1. **Health check:**
   - Open browser: http://localhost:8000/health
   - Should return: `{"status":"healthy"}`

2. **API Documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Root endpoint:**
   - http://localhost:8000/
   - Should return: `{"message":"Healthcare Wellness & Preventive Care Portal API"}`

## All Available Routes

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get token

### User Management
- `DELETE /users/me` - Delete account (requires auth)

### Goals (Patient only)
- `POST /goals` - Add/update daily goal
- `GET /goals/today` - Get today's goal
- `GET /goals/history` - Get past week's goals

### Credentials
- `PUT /credentials/modify` - Update credentials (requires auth)

### Provider (Provider only)
- `GET /provider/patients` - List assigned patients
- `GET /provider/patient/{id}/goals` - Get patient goals
- `GET /provider/patient/{id}/status` - Get patient status

## Troubleshooting

### Port 8000 already in use:
Change the port in `main.py` or use:
```bash
uvicorn main:app --reload --port 8001
```

### MongoDB connection error:
- Check if MongoDB is running
- Verify MONGODB_URI in .env file
- For local MongoDB, ensure it's started: `mongod`

### Import errors:
- Make sure you're in the `backend` directory
- Install all dependencies: `pip install -r requirements.txt`

## Notes

- The server will start even if MongoDB is not connected
- Database connection errors will occur when accessing routes that use the database
- Check the terminal for any error messages

