"""
API Management Service for Diagnyx Platform

This service provides API management capabilities including:
- API registration and configuration
- API documentation management
- API versioning
- API analytics integration
- API health checks
- Contact form submissions
- Newsletter subscriptions
- Trial waitlist management
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Dict, Any, List, Optional
import time
import uuid
import psycopg2
from psycopg2.extras import RealDictCursor

# Models
class ApiRegistrationRequest(BaseModel):
    name: str
    description: str
    base_url: str
    version: str
    owner_id: str
    documentation_url: Optional[str] = None
    tags: List[str] = []

class ApiResponse(BaseModel):
    api_id: str
    name: str
    description: str
    base_url: str
    version: str
    owner_id: str
    documentation_url: Optional[str] = None
    tags: List[str] = []
    created_at: str
    updated_at: str

class HealthCheckResult(BaseModel):
    check_id: str
    api_id: str
    status: str
    response_time: float
    timestamp: int
    details: Dict[str, Any]

class ContactSubmission(BaseModel):
    email: EmailStr
    name: str
    subject: str
    message: str
    company: Optional[str] = None

class NewsletterSubscription(BaseModel):
    email: EmailStr

class TrialWaitlistEntry(BaseModel):
    email: EmailStr
    full_name: str
    company: Optional[str] = None
    selected_plan: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    uptime: float
    service: str
    database: str

class ServiceStatusResponse(BaseModel):
    service: str
    timestamp: str
    database: str
    status: str
    message: str

# Database configuration
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "api-management-db"
DB_USER = "dev"
DB_PASSWORD = "dev"

# Create FastAPI app
app = FastAPI(
    title="Diagnyx API Management Service",
    description="API management service for the Diagnyx platform",
    version="1.0.0"
)

# Store start time for uptime calculation
start_time = time.time()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "API Management Service",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    # Database connection check
    db_status = "UP"
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        conn.close()
    except Exception:
        db_status = "DOWN"
        
    return HealthResponse(
        status="UP",
        version="1.0.0", 
        uptime=time.time() - start_time,
        service="api-management-service",
        database=db_status
    )

@app.get("/service-status", response_model=ServiceStatusResponse)
async def service_status():
    """Service status endpoint for database connectivity check"""
    db_status = "UP"
    status = "SUCCESS"
    message = "API Management Service is operational with database connectivity"
    
    try:
        # Attempt to connect to the database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
    except Exception as e:
        db_status = "DOWN"
        status = "FAILURE"
        message = f"API Management Service is degraded - database connectivity issue: {str(e)}"
    
    return ServiceStatusResponse(
        service="api-management-service",
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
        database=db_status,
        status=status,
        message=message
    )

@app.post("/api/v1/apis", response_model=ApiResponse)
async def register_api(request: ApiRegistrationRequest):
    """Register a new API"""
    api_id = str(uuid.uuid4())
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # In a real implementation, this would save to the database
    # For now, we'll just return a mock response
    return ApiResponse(
        api_id=api_id,
        name=request.name,
        description=request.description,
        base_url=request.base_url,
        version=request.version,
        owner_id=request.owner_id,
        documentation_url=request.documentation_url,
        tags=request.tags,
        created_at=current_time,
        updated_at=current_time
    )

@app.get("/api/v1/apis/{api_id}", response_model=ApiResponse)
async def get_api(api_id: str):
    """Get API details by ID"""
    # In a real implementation, this would fetch from the database
    # For now, we'll return a mock response
    if not api_id:
        raise HTTPException(status_code=404, detail="API not found")
    
    return ApiResponse(
        api_id=api_id,
        name="Sample API",
        description="This is a sample API",
        base_url="https://api.example.com",
        version="1.0.0",
        owner_id="user-123",
        documentation_url="https://docs.example.com",
        tags=["sample", "example"],
        created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=time.strftime("%Y-%m-%d %H:%M:%S")
    )

@app.get("/api/v1/apis", response_model=Dict[str, Any])
async def list_apis():
    """List all registered APIs"""
    # In a real implementation, this would fetch from the database
    # For now, we'll return a mock response
    apis = [
        ApiResponse(
            api_id=str(uuid.uuid4()),
            name=f"Sample API {i}",
            description=f"This is a sample API {i}",
            base_url=f"https://api{i}.example.com",
            version="1.0.0",
            owner_id="user-123",
            documentation_url=f"https://docs{i}.example.com",
            tags=["sample", "example"],
            created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        for i in range(1, 4)
    ]
    
    return {
        "data": apis,
        "total": len(apis)
    }

@app.put("/api/v1/apis/{api_id}", response_model=ApiResponse)
async def update_api(api_id: str, request: ApiRegistrationRequest):
    """Update an existing API"""
    # In a real implementation, this would update in the database
    # For now, we'll return a mock response
    if not api_id:
        raise HTTPException(status_code=404, detail="API not found")
    
    return ApiResponse(
        api_id=api_id,
        name=request.name,
        description=request.description,
        base_url=request.base_url,
        version=request.version,
        owner_id=request.owner_id,
        documentation_url=request.documentation_url,
        tags=request.tags,
        created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=time.strftime("%Y-%m-%d %H:%M:%S")
    )

@app.delete("/api/v1/apis/{api_id}")
async def delete_api(api_id: str):
    """Delete an API"""
    # In a real implementation, this would delete from the database
    # For now, we'll return a mock response
    if not api_id:
        raise HTTPException(status_code=404, detail="API not found")
    
    return {"message": f"API {api_id} deleted successfully"}

@app.get("/api/v1/apis/{api_id}/health-checks", response_model=Dict[str, Any])
async def get_api_health_checks(api_id: str):
    """Get health check results for an API"""
    # In a real implementation, this would fetch from the database
    # For now, we'll return a mock response
    health_checks = [
        {
            "check_id": str(uuid.uuid4()),
            "api_id": api_id,
            "status": "healthy" if i % 3 != 0 else "degraded",
            "response_time": 0.5 + (i * 0.1),
            "timestamp": int(time.time()) - (i * 3600),
            "details": {
                "status_code": 200 if i % 3 != 0 else 500,
                "response_size": 1024,
                "endpoint": "/api/v1/resource"
            }
        }
        for i in range(5)
    ]
    
    return {
        "data": health_checks,
        "total": len(health_checks)
    }

@app.post("/api/v1/contact-submissions", status_code=201)
async def submit_contact_form(submission: ContactSubmission):
    """Submit a contact form"""
    # In a real implementation, this would save to the database
    # For now, we'll just return a mock response
    return {
        "message": "Contact form submitted successfully",
        "submission_id": str(uuid.uuid4())
    }

@app.post("/api/v1/newsletter-subscriptions", status_code=201)
async def subscribe_newsletter(subscription: NewsletterSubscription):
    """Subscribe to the newsletter"""
    # In a real implementation, this would save to the database
    # For now, we'll just return a mock response
    return {
        "message": "Subscribed to newsletter successfully",
        "subscription_id": str(uuid.uuid4())
    }

@app.post("/api/v1/trial-waitlist", status_code=201)
async def join_trial_waitlist(entry: TrialWaitlistEntry):
    """Join the trial waitlist"""
    # In a real implementation, this would save to the database
    # For now, we'll just return a mock response
    return {
        "message": "Added to trial waitlist successfully",
        "waitlist_id": str(uuid.uuid4())
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8086) 