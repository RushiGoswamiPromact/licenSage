import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.dependency_file import router as dependency_router
from backend.routes.github import router as github_router
from backend.utils.logger_utils import get_logger

logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="LicenSage API",
    description="API for analyzing software licenses",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(github_router, prefix="/api/github", tags=["GitHub"])
app.include_router(dependency_router, prefix="/api/dependency", tags=["Dependency"])


@app.get("/", tags=["Root"])
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to LicenSage API"}


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
