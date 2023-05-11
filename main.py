from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount the static files from the current directory
app.mount("/3266_/", StaticFiles(directory="/root/phys2236/"), name="static")
