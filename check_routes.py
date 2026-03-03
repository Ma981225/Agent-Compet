"""
检查FastAPI路由注册情况
"""
from app import app

print("=" * 60)
print("检查FastAPI路由注册情况")
print("=" * 60)
print("\n已注册的路由:")
for route in app.routes:
    if hasattr(route, "path") and hasattr(route, "methods"):
        methods = ", ".join(route.methods) if route.methods else "GET"
        print(f"  {methods:15} {route.path}")
    elif hasattr(route, "path"):
        print(f"  {'N/A':15} {route.path}")

print("\n" + "=" * 60)
print("检查完成")
print("=" * 60)