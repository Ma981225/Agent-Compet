"""
检查路由注册情况
"""
import sys
sys.path.insert(0, '.')

from app import app

print("=" * 60)
print("检查已注册的路由:")
print("=" * 60)

for route in app.routes:
    if hasattr(route, "path") and hasattr(route, "methods"):
        methods = ", ".join(route.methods) if route.methods else "GET"
        print(f"  {methods:8s} {route.path}")
    elif hasattr(route, "path"):
        print(f"  {'':8s} {route.path}")

print("=" * 60)
print("\n关键路由检查:")
print(f"  /api/v1/chat 存在: {any(r.path == '/api/v1/chat' for r in app.routes if hasattr(r, 'path'))}")
print(f"  /api/v1/reset 存在: {any(r.path == '/api/v1/reset' for r in app.routes if hasattr(r, 'path'))}")
print("=" * 60)