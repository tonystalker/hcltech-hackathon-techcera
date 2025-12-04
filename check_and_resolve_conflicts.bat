@echo off
echo ========================================
echo Conflict Check and Resolution Helper
echo ========================================
echo.

cd /d %~dp0

echo Step 1: Checking for conflict markers in code...
findstr /S /C:"<<<<<<< HEAD" backend\*.py 2>nul
if errorlevel 1 (
    echo   [OK] No conflict markers found in Python files
) else (
    echo   [CONFLICT] Conflict markers found! Check files above.
)

echo.
echo Step 2: Fetching latest changes...
git fetch origin master

echo.
echo Step 3: Checking merge status...
git status

echo.
echo ========================================
echo Instructions:
echo ========================================
echo.
echo If conflicts are found:
echo   1. Open the conflicted file
echo   2. Look for: ^<^<^<^<^<^<^< HEAD markers
echo   3. Resolve by keeping your changes or merging
echo   4. Remove all conflict markers
echo   5. Run: git add [filename]
echo   6. Run: git commit
echo.
echo If no conflicts:
echo   - You're ready to push!
echo.
pause

