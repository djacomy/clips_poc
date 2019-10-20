"""
For local development, use a .env file to set
environment variables.
"""
import os
from environs import Env

BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)))
PROJECT_ROOT = os.path.join(BASE_DIR, os.pardir)

env = Env()
env.read_env(PROJECT_ROOT)


ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")

MAPBOX_ACCESS_KEY = env.str("MAPBOX_ACCESS_KEY")
