from importlib import import_module
import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse

app = FastAPI()

# API routes
def load_routes():
    """
    Loads all the routes of the api
    """
    path = "./routes/"
    files = list(filter(lambda x: x.endswith(".py"), os.listdir(path)))
    print(files)
    for file in files:
        route_name = file.split("/")[-1][:-3]
        print(route_name)
        module_path = file[:-3]
        print(f"routes.{module_path}")
        module = import_module(f"routes.{module_path}")
        app.include_router(module.router, prefix=f"/api/{route_name}")

load_routes()

for route in app.routes:
    print(1, route)

# Client catch-all route for SPA
@app.get("/{full_path:path}")
async def catch_all(request: Request, full_path: str):
    print("in catch all")
    if '.' in full_path:
        return FileResponse(f"./client/dist/{full_path}")
    return FileResponse("./client/dist/index.html")

for route in app.routes:
    print(2, route)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)