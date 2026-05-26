from contextlib import asynccontextmanager

import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import habit, ai, checkin, user, common
from app.core.database import create_indexes
from app.core.exception_handler import http_exception_handler, general_exception_handler
from app.models.common import ApiResponse


@asynccontextmanager
async def lifespan(app):
    await create_indexes()
    yield


app = FastAPI(
    title="极律 UltraFlow API",
    description="AI习惯养成应用后端服务",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(user.router, prefix="/api")
app.include_router(habit.router, prefix="/api")
app.include_router(checkin.router, prefix="/api")
app.include_router(ai.router, prefix="/api")
app.include_router(common.router, prefix="/api")

# Serve uploaded files
uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")


@app.get("/")
async def root():
    return ApiResponse(msg="极律 UltraFlow API v1.0.0").model_dump()


@app.get("/health")
async def health_check():
    return ApiResponse(msg="healthy").model_dump()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
