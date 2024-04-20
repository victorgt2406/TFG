"Load all the routes of the middleware"
from importlib import import_module
import os
from fastapi import FastAPI


def load_routes(app: FastAPI) -> None:
    """
    Loads all the routes of the api
    """
    path = "./routes/"
    files = list(filter(
        lambda x: x.endswith(".py") and not x.endswith("__init__.py"),
        os.listdir(path)
    ))
    for file in files:
        route_name = file.split("/")[-1][:-3]
        module_path = file[:-3]
        module = import_module(f"routes.{module_path}")
        app.include_router(module.router, prefix=f"/api/{route_name}")
        print(f"/api/{route_name} loaded")
