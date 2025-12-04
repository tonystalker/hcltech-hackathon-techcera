# Git Push Instructions

## New Branch: `routes/provider`

### Files to be Committed (excluding .md files):

#### Routes:
- `backend/routes/provider.py` - Provider routes (NEW)
- `backend/routes/credentials.py` - Credentials modification route (NEW)
- `backend/routes/goals.py` - Goals route with steps, sleep, water tracking
- `backend/routes/auth.py` - Updated with email normalization
- `backend/routes/user.py` - Delete account route

#### Models & Dependencies:
- `backend/models/models.py` - Added Goal models, UserUpdate, PatientListItem, PatientStatusResponse
- `backend/dependencies.py` - Added get_current_provider dependency

#### Configuration:
- `backend/main.py` - Registered all new routers

#### Helper Files:
- `backend/test_routes.py` - Route testing script
- `backend/check_routes.py` - Route verification script
- `backend/start_server.py` - Server startup script
- `backend/start.bat` - Windows batch file to start server

**Note:** Documentation files (.md) are excluded from commit

---

## Quick Push (Automated)

**Option 1: Use the batch file (Windows)**
```bash
git_push_new_branch.bat
```

**Option 2: Manual commands**

```bash
# Create and switch to new branch
git checkout -b routes/provider

# Add specific files (excluding .md files)
git add backend/routes/
git add backend/models/
git add backend/dependencies.py
git add backend/main.py
git add backend/test_routes.py
git add backend/check_routes.py
git add backend/start_server.py
git add backend/start.bat

# Commit
git commit -m "Add provider routes, credentials route, goals route, and helper files"

# Push to remote
git push -u origin routes/provider
```

---

## What's Being Added:

### New Routes:
1. **Provider Routes** (`/provider`):
   - GET `/provider/patients` - List assigned patients
   - GET `/provider/patient/{id}/goals` - Get patient goals
   - GET `/provider/patient/{id}/status` - Get patient status

2. **Credentials Route** (`/credentials`):
   - PUT `/credentials/modify` - Modify user credentials

3. **Goals Routes** (`/goals`):
   - POST `/goals` - Add/update daily goal (steps, sleep, water)
   - GET `/goals/today` - Get today's goal
   - GET `/goals/history` - Get past week's goals

### Updates:
- Enhanced auth routes with email normalization
- Added role-based access control
- Improved error handling

---

## After Pushing:

The branch will be available at:
```
https://github.com/tonystalker/hcltech-hackathon-techcera/tree/routes/provider
```

You can create a pull request from there!
