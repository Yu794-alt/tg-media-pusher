import os
import sys

print("="*40)
print(" 🔍 ENVIRONMENT VARIABLES")
print("="*40)

for key in sorted(os.environ):
    if "FLASK" in key or "PYTHON" in key:
        print(f"{key} = {os.environ[key]}")

print("\n" + "="*40)
print(" 🔍 sys.path (PYTHONPATH)")
print("="*40)
for p in sys.path:
    print(p)

print("\n" + "="*40)
print(" 🔍 CURRENT WORKING DIR")
print("="*40)
print(os.getcwd())

print("\n" + "="*40)
print(" 🔍 .env file content (if exists)")
print("="*40)
try:
    with open(".env") as f:
        print(f.read())
except FileNotFoundError:
    print("No .env file found.")

print("\n" + "="*40)
print(" 🔍 FLASK_APP location resolution")
print("="*40)
flask_app = os.environ.get("FLASK_APP")
if flask_app:
    print(f"FLASK_APP is set to: {flask_app}")
    module_path = flask_app.split(":")[0]
    try:
        __import__(module_path)
        print(f"✅ Module '{module_path}' successfully imported")
    except ImportError as e:
        print(f"❌ ImportError: {e}")
else:
    print("FLASK_APP is not set.")
