from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import tasks, agents, auth
from app.database.session import engine
from app.models import Base
from app.middleware.auth import AuthMiddleware
from app.middleware.logging import LoggingMiddleware

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered Todo Application API",
    version=settings.API_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add logging middleware first (so it captures all requests)
app.add_middleware(LoggingMiddleware)

# Add custom auth middleware
app.add_middleware(AuthMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # expose_headers=["Access-Control-Allow-Origin"]
)

# Include API routes
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(agents.router, prefix="/api", tags=["agents"])
app.include_router(auth.router, prefix="/api", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "AI Todo Application API", "version": settings.API_VERSION}

@app.get("/health")
def health_check():
    return {"status": "healthy", "api_version": settings.API_VERSION}