import sys
print("Python version:", sys.version)
print("Current working directory:", sys.path[0])

try:
    from app.core.db import SessionLocal
    print("Successfully imported SessionLocal")
    
    try:
        from app.models.services import Service
        print("Successfully imported Service model")
    except Exception as e:
        print(f"Error importing Service model: {e}")
        
except Exception as e:
    print(f"Error importing SessionLocal: {e}")
    import traceback
    traceback.print_exc()