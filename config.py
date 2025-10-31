"""
Configuration file for SPTool
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'
    HOST = os.environ.get('HOST', '127.0.0.1')
    PORT = int(os.environ.get('PORT', 5000))
    
    # OpenAI API settings (optional - for AI-powered diagnosis)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    
    # Security settings
    REQUIRE_CONFIRMATION = True  # Always require user confirmation before executing fixes
    LOG_ACTIONS = True  # Log all executed commands
    LOG_FILE = 'sptool_actions.log'
    
    # Thresholds for issue detection
    CPU_THRESHOLD = 90  # % CPU usage to trigger warning
    MEMORY_THRESHOLD = 85  # % Memory usage to trigger warning
    DISK_THRESHOLD = 90  # % Disk usage to trigger warning
    TEMP_THRESHOLD = 80  # °C CPU temperature threshold (if available)

