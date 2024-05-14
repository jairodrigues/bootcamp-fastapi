from fastapi import FastAPI
from app.middlewares.logger import request_middleware
from .routers import assistant, health_check, generative
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Assistentes AI")

@app.middleware("http")
async def middleware_handler(request, call_next):
    return await request_middleware(request, call_next)

app.include_router(assistant.router)
app.include_router(health_check.router)
app.include_router(generative.router)