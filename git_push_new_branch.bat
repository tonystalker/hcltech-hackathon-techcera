@echo off
echo Creating new branch and pushing changes...
echo.

cd /d %~dp0

echo Step 1: Creating new branch 'routes/provider'...
git checkout -b routes/provider

echo.
echo Step 2: Adding all changes (excluding .md files)...
git add backend/routes/provider.py
git add backend/routes/credentials.py
git add backend/routes/goals.py
git add backend/routes/auth.py
git add backend/routes/user.py
git add backend/models/models.py
git add backend/dependencies.py
git add backend/main.py
git add backend/test_routes.py
git add backend/check_routes.py
git add backend/start_server.py
git add backend/start.bat

echo.
echo Step 3: Committing changes...
git commit -m "Add provider routes, credentials route, goals route, and helper files"

echo.
echo Step 4: Pushing to remote...
git push -u origin routes/provider

echo.
echo Done! New branch 'routes/provider' created and pushed.
pause

