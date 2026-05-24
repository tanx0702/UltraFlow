from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import habit, ai, checkin, user

app = FastAPI(
    title="极律 UltraFlow API",
    description="AI习惯养成应用后端服务",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router, prefix="/api")
app.include_router(habit.router, prefix="/api")
app.include_router(checkin.router, prefix="/api")
app.include_router(ai.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "极律 UltraFlow API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
