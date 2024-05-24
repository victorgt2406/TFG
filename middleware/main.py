"Middleware application"

import os
import threading
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse

from config import OllamaSingleton, OpenSearchSingleton
from file_observer import file_observer
from routes import load_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    await OpenSearchSingleton.test_connection()
    await OllamaSingleton.test_connection()
    yield

app = FastAPI(lifespan=lifespan)

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
# Get the directory of app.py
app_dir = os.path.dirname(os.path.abspath(__file__))
client_dist_dir = os.path.join(
    app_dir, 'client', 'dist')  # Path to client/dist

load_routes(app)

# Client catch-all route for SPA


@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    "All routes that does not start with /api/ return the client"
    if full_path.startswith("api") and not full_path.endswith("/"):
        return RedirectResponse(url=f"/{full_path}/")
    elif full_path.startswith("api"):
        raise HTTPException(status_code=404)
    if "." in full_path:
        if full_path == "favicon.ico":
            return FileResponse(os.path.join(client_dist_dir, "favicon.svg"))
        else:
            return FileResponse(os.path.join(client_dist_dir, full_path))
    try:
        def get_web():
            return f"{full_path}{'' if not full_path else '/'}index.html"

        return FileResponse(os.path.join(client_dist_dir, get_web()))
    except Exception as e:
        # return FileResponse(os.path.join(client_dist_dir,"404/index.html"))
        raise HTTPException(status_code=404) from e

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("MDW_PORT") or 2002)  # type: ignore

    # Prepare and start the file watcher in a daemon thread
    watcher_thread = threading.Thread(
        target=file_observer, args=(), daemon=True)
    watcher_thread.start()

    print(f"Running API at http://localhost:{port} 🚀")
    uvicorn.run(app, host="0.0.0.0", port=port)
