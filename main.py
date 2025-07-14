import click
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from mongoengine import connect
from app.dependencies import get_mongo_uri

from app.api.bed_routes import router as bed_router
from app.api.plant_family_routes import router as plant_family_router

# Load environment variables
load_dotenv("local.env")


# Connect to mongoengine
connect(host=get_mongo_uri(), db="grow")

# Create FastAPI app
app = FastAPI(
    title="GROW Backend API",
    description="Backend API for the GROW garden planning application",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(bed_router)
app.include_router(plant_family_router)


@app.get("/")
async def root():
    return {"message": "GROW Backend API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@click.command()
@click.option("--reload", is_flag=True, default=False)
def main(reload: bool):
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=reload)


if __name__ == "__main__":
    main()
