"""Configuration module for the application."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# API configuration
API_V1_STR = "/api/v1"
PROJECT_NAME = "Glucose Levels API"

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/glucose.db")

# Application settings
DEFAULT_PAGE_SIZE = 100
MAX_PAGE_SIZE = 1000