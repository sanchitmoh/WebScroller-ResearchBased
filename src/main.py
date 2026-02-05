"""
ALCIS Main Application Entry Point
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.config import ConfigManager
from core.logging import get_logger, get_structured_logger
from core.exceptions import ALCISException

# Initialize FastAPI app
app = FastAPI(
    title="ALCIS - AI-Driven Autonomous Learning & Certification Interaction System",
    description="A Research Prototype for Automation, Security Testing, and Vulnerability Assessment",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize components
config_manager = ConfigManager()
logger = get_logger("alcis.main")
struct_logger = get_structured_logger("alcis.main")

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("Starting ALCIS application")
    struct_logger.info("application_startup", version="1.0.0")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Shutting down ALCIS application")
    struct_logger.info("application_shutdown")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to ALCIS - AI-Driven Autonomous Learning & Certification Interaction System",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Basic health checks
        config_status = config_manager is not None
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "healthy",
                "version": "1.0.0",
                "components": {
                    "configuration": "ok" if config_status else "error",
                    "logging": "ok",
                    "application": "ok"
                }
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )

@app.get("/api/v1/status")
async def api_status():
    """API status endpoint"""
    return {
        "api_version": "v1",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.exception_handler(ALCISException)
async def alcis_exception_handler(request, exc: ALCISException):
    """Handle ALCIS custom exceptions"""
    logger.error(f"ALCIS Exception: {exc.message}", extra={
        "error_code": exc.error_code,
        "details": exc.details
    })
    
    return JSONResponse(
        status_code=400,
        content={
            "error": exc.message,
            "error_code": exc.error_code,
            "details": exc.details
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )