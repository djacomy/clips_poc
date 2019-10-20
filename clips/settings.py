"""
For local development, use a .env file to set
environment variables.
"""
import os
from environs import Env

BASE_DIR = os.path.join("..", os.path.abspath(os.path.dirname(__file__)))

env = Env()
env.read_env(BASE_DIR)


ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")

MAPBOX_ACCESS_KEY = env.str("MAPBOX_ACCESS_KEY")
