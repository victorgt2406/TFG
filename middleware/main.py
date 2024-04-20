import os
import threading

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse

from file_observer import file_observer
from routes import load_routes

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:2002", "http://localhost:3000"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
app_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of app.py
client_dist_dir = os.path.join(app_dir, 'client', 'dist')  # Path to client/dist

load_routes(app)

# Client catch-all route for SPA
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    "All routes that does not start with /api/ return the client"
    if full_path.startswith("api") and not full_path.endswith("/"):
        return RedirectResponse(url=f"/{full_path}/")
    else:
        raise HTTPException(status_code=404)
    if '.' in full_path:
        return FileResponse(os.path.join(client_dist_dir, full_path))
    return FileResponse(os.path.join(client_dist_dir,"index.html"))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("MDW_PORT") or 2002) # type: ignore

    # Prepare and start the file watcher in a daemon thread
    watcher_thread = threading.Thread(target=file_observer, args=(), daemon=True)
    watcher_thread.start()

    print(f"Running API at http://localhost:{port} 🚀")
    uvicorn.run(app, host="0.0.0.0", port=port)