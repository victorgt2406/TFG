import os
import threading
from fastapi import FastAPI
from fastapi.responses import FileResponse
from routes import load_routes
from dotenv import load_dotenv
from file_observer import file_observer
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
app = FastAPI()
app_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of app.py
client_dist_dir = os.path.join(app_dir, 'client', 'dist')  # Path to client/dist

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
    port = int(os.getenv("MDW_PORT") or 2002) # type: ignore

    # Prepare and start the file watcher in a daemon thread
    watcher_thread = threading.Thread(target=file_observer, args=(), daemon=True)
    watcher_thread.start()

    print(f"Running API at http://localhost:{port} 🚀")
    uvicorn.run(app, host="0.0.0.0", port=port)