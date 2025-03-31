from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import shape_analyzer

app = FastAPI(
    title="ShapeSnap API",
    description="API for body shape analysis and fitness tracking",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    shape_analyzer.router,
    prefix="/api/v1/shape-analyzer",
    tags=["shape-analyzer"]
)

@app.get("/")
async def root():
    return {"message": "Welcome to ShapeSnap API"} 