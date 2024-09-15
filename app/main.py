from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.domain.db import init_db
from app.api.auth import router as auth_routes
from app.api.book import router as book_routes
from app.config import settings
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Create the FastAPI app
app = FastAPI()

origins = [
    "http://localhost:3000",  # React development server
    # Add other origins as needed
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include the authentication routes
app.include_router(auth_routes)
app.include_router(book_routes)


# Startup event to create tables when the app starts
@app.on_event("startup")
def on_startup():
    init_db()
    logger.info(f"Database connected: {settings.DATABASE_URL}")
    logger.info("Database tables checked/created.")
