@echo off
echo ========================================
echo Conflict Resolution Script
echo ========================================
echo.

cd /d %~dp0

echo Step 1: Checking current branch...
git branch --show-current

echo.
echo Step 2: Fetching latest changes from remote...
git fetch origin

echo.
echo Step 3: Checking for conflicts with master...
git merge-base HEAD origin/master
if errorlevel 1 (
    echo No common ancestor found
) else (
    echo Common ancestor found
)

echo.
echo Step 4: Attempting to merge origin/master...
git merge origin/master --no-commit --no-ff

if errorlevel 1 (
    echo.
    echo ========================================
    echo CONFLICTS DETECTED!
    echo ========================================
    echo.
    echo Checking which files have conflicts...
    git status
    
    echo.
    echo Conflicts found. Please resolve them manually.
    echo Run: git status to see which files need attention
) else (
    echo.
    echo ========================================
    echo No conflicts found!
    echo ========================================
    echo.
    git merge --abort
    echo Merge test completed. No conflicts detected.
)

echo.
pause

