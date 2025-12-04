"""
Simple script to start the FastAPI server
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Starting FastAPI server...")
    print("=" * 60)
    
    # Import and start server
    import uvicorn
    from main import app
    
    print("✅ Server imports successful!")
    print("✅ All routes loaded!")
    print("\nStarting server on http://localhost:8000")
    print("API docs will be available at http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Start server
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nPlease install dependencies:")
    print("  pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

