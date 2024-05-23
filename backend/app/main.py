from app.v1 import v1
from fastapi import FastAPI

app = FastAPI()

app.include_router(v1.router, prefix="/api")
