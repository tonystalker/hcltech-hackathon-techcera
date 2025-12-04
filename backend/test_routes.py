"""
Test script to verify all routes are working correctly
"""
import sys
import traceback


def test_imports():
    """Test that all routes can be imported without errors"""
    print("Testing route imports...")

    try:
        print("  ✓ Testing auth route...")
        from routes.auth import router as auth_router
        print("    ✓ Auth router imported successfully")

        print("  ✓ Testing user route...")
        from routes.user import router as user_router
        print("    ✓ User router imported successfully")

        print("  ✓ Testing goals route...")
        from routes.goals import router as goals_router
        print("    ✓ Goals router imported successfully")

        print("  ✓ Testing credentials route...")
        from routes.credentials import router as credentials_router
        print("    ✓ Credentials router imported successfully")

        print("  ✓ Testing provider route...")
        from routes.provider import router as provider_router
        print("    ✓ Provider router imported successfully")

        print("  ✓ Testing main app...")
        from main import app
        print("    ✓ Main app imported successfully")

        print("\n✅ All routes imported successfully!")

        # Check routes
        print("\n📋 Checking registered routes...")
        routes = []
        for route in app.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                routes.append(f"{', '.join(route.methods)} {route.path}")

        print(f"\nFound {len(routes)} routes:")
        for route in sorted(routes):
            print(f"  • {route}")

        return True

    except Exception as e:
        print(f"\n❌ Error importing routes: {str(e)}")
        traceback.print_exc()
        return False


def test_models():
    """Test that all models can be imported"""
    print("\nTesting model imports...")

    try:
        from models.models import (
            UserCreate, UserResponse, UserUpdate,
            LoginRequest, TokenResponse,
            GoalCreate, GoalResponse,
            PatientListItem, PatientStatusResponse
        )
        print("  ✓ All models imported successfully")
        return True
    except Exception as e:
        print(f"  ❌ Error importing models: {str(e)}")
        traceback.print_exc()
        return False


def test_dependencies():
    """Test that all dependencies can be imported"""
    print("\nTesting dependency imports...")

    try:
        from dependencies import (
            get_current_user,
            get_current_patient,
            get_current_provider,
            SECRET_KEY,
            ALGORITHM,
            ACCESS_TOKEN_EXPIRE_HOURS
        )
        print("  ✓ All dependencies imported successfully")
        return True
    except Exception as e:
        print(f"  ❌ Error importing dependencies: {str(e)}")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Healthcare Portal Backend Routes")
    print("=" * 60)

    results = []

    results.append(("Models", test_models()))
    results.append(("Dependencies", test_dependencies()))
    results.append(("Routes", test_imports()))

    print("\n" + "=" * 60)
    print("Test Results Summary:")
    print("=" * 60)

    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {name}: {status}")
        if not result:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("✅ All tests passed! Routes are ready to use.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please fix the errors above.")
        sys.exit(1)
