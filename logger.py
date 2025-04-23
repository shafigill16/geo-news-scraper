# logger.py
import logging
import os

# Get the desired log level from environment variable, defaulting to 'INFO'
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Configure the root logger
logging.basicConfig(
    level=LOG_LEVEL,  # Set log level (e.g., DEBUG, INFO, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",  # Format of log messages
    handlers=[
        logging.StreamHandler()  # Output logs to the console (stdout)
    ]
)

# Create a named logger for the application
logger = logging.getLogger("GeoNewsApp")
