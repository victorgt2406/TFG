import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from routes import load_routes

app = FastAPI()
app_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of app.py
client_dist_dir = os.path.join(app_dir, 'client', 'dist')  # Path to your client/dist

load_routes(app)


@app.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    "Return the favicon of the server"
    return FileResponse(os.path.join(client_dist_dir, 'vite.svg'))

# Client catch-all route for SPA
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    "All routes that does not start with /api/ return the client"
    if '.' in full_path:
        return FileResponse(os.path.join(client_dist_dir, full_path))
    return FileResponse(os.path.join(client_dist_dir,"index.html"))

if __name__ == "__main__":
    import uvicorn
    port = 3000
    print(f"Running API at http://localhost:{port} 🚀")
    uvicorn.run(app, host="0.0.0.0", port=port)