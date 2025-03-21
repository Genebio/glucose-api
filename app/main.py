"""Main application module."""
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import PROJECT_NAME
from app.interfaces.api.v1 import router as api_v1_router
from app.infrastructure.database import Base, engine


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_tables():
    """Create database tables."""
    Base.metadata.create_all(bind=engine)


def get_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI application
    """
    # Create database tables
    create_tables()
    
    # Create FastAPI application
    application = FastAPI(
        title=PROJECT_NAME,
        description="API for managing glucose levels data",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # Add CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, restrict this to specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routers
    application.include_router(api_v1_router)
    
    # Global exception handler
    @application.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Global exception handler."""
        logger.exception(f"Unhandled exception: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal server error",
                "data": None
            },
        )
    
    # Health check endpoint
    @application.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy"}
    
    return application


app = get_application()