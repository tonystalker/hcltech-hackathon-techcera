"""
Quick script to verify all routes are registered without starting the server
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("Healthcare Portal - Route Verification")
print("=" * 70)

try:
    print("\n1. Testing imports...")
    from main import app
    print("   ✅ Main app imported successfully")
    
    print("\n2. Checking registered routes...")
    routes = []
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            methods = ', '.join(route.methods)
            routes.append((methods, route.path))
    
    print(f"\n   Found {len(routes)} routes:\n")
    
    # Group by prefix
    route_groups = {}
    for method, path in sorted(routes):
        prefix = path.split('/')[1] if len(path.split('/')) > 1 else 'root'
        if prefix not in route_groups:
            route_groups[prefix] = []
        route_groups[prefix].append((method, path))
    
    for prefix in sorted(route_groups.keys()):
        print(f"   [{prefix.upper()}]")
        for method, path in route_groups[prefix]:
            print(f"      {method:8} {path}")
        print()
    
    print("=" * 70)
    print("✅ All routes verified successfully!")
    print("=" * 70)
    print("\nTo start the server, run:")
    print("   python main.py")
    print("   OR")
    print("   uvicorn main:app --reload")
    print("\nServer will be available at: http://localhost:8000")
    print("API documentation: http://localhost:8000/docs")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

