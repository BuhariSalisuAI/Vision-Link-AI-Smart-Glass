# helpers.py
# Vision-Link AI Smart Glass - Utility Helper Functions

import os
import json
import logging
import time
from datetime import datetime

# Setup logging
def setup_logging(log_file='logs/vision_link.log'):
    """
    Setup logging configuration
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# Logger instance
logger = setup_logging()

def log_error(error_message, exception=None):
    """
    Log an error with optional exception details
    """
    if exception:
        logger.error(f"{error_message}: {str(exception)}")
    else:
        logger.error(error_message)

def log_info(message):
    """
    Log an info message
    """
    logger.info(message)

def get_timestamp():
    """
    Get current timestamp in readable format
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def save_json(data, filename):
    """
    Save data to JSON file
    """
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Data saved to {filename}")
        return True
    except Exception as e:
        log_error(f"Failed to save {filename}", e)
        return False

def load_json(filename):
    """
    Load data from JSON file
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Data loaded from {filename}")
        return data
    except Exception as e:
        log_error(f"Failed to load {filename}", e)
        return None

def ensure_directory(path):
    """
    Create directory if it doesn't exist
    """
    os.makedirs(path, exist_ok=True)
    return path

def format_time(seconds):
    """
    Format seconds into readable time string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

def truncate_text(text, max_length=100):
    """
    Truncate text to maximum length
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def is_valid_phone_number(number):
    """
    Check if phone number is valid (Nigerian format)
    """
    # Remove spaces and +
    number = number.replace(' ', '').replace('+', '')
    
    # Nigerian numbers: 234 followed by 10 digits, or 0 followed by 10 digits
    if number.startswith('234') and len(number) == 13:
        return True
    if number.startswith('0') and len(number) == 11:
        return True
    
    return False

def format_phone_number(number):
    """
    Format phone number to international format
    """
    number = number.replace(' ', '').replace('-', '')
    
    if number.startswith('0'):
        return '+234' + number[1:]
    elif number.startswith('234'):
        return '+' + number
    elif number.startswith('+'):
        return number
    
    return '+234' + number

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two GPS coordinates (Haversine formula)
    Returns distance in meters
    """
    from math import radians, cos, sin, asin, sqrt
    
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in meters
    r = 6371000
    
    return c * r

def retry_function(func, max_retries=3, delay=1):
    """
    Retry a function multiple times with delay
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise
    
    return None

def get_system_info():
    """
    Get system information
    """
    import platform
    
    info = {
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'timestamp': get_timestamp()
    }
    
    return info

if __name__ == "__main__":
    # Test helpers
    print("=== Testing Helpers ===")
    
    log_info("Test info message")
    log_error("Test error message")
    
    print(f"Timestamp: {get_timestamp()}")
    print(f"Formatted time: {format_time(3665)}")
    print(f"Truncated text: {truncate_text('This is a very long text that needs truncation', 20)}")
    print(f"Valid phone: {is_valid_phone_number('+2348012345678')}")
    print(f"Distance: {calculate_distance(12.0, 8.0, 12.1, 8.1):.0f} meters")
    print(f"System info: {get_system_info()}")
              
