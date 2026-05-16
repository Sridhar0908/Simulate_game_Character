"""
Utility functions for the application.
"""

import re
from datetime import datetime

def is_valid_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def format_datetime(dt: datetime) -> str:
    """Format datetime for display."""
    if not dt:
        return "Never"
    return dt.strftime("%B %d, %Y at %I:%M %p")

def sanitize_filename(text: str, max_length: int = 50) -> str:
    """Create safe filename from text."""
    safe = "".join(c if c.isalnum() or c in " _-" else "_" for c in text)
    safe = safe.strip().replace(" ", "_")
    return safe[:max_length]

def estimate_generation_time() -> int:
    """Estimate generation time in seconds."""
    return 180  # Hunyuan3D-2 takes ~2-3 minutes

def get_status_color(status: str) -> str:
    """Get color code for status."""
    colors = {
        'pending': 'warning',
        'processing': 'info',
        'completed': 'success',
        'failed': 'error'
    }
    return colors.get(status, 'default')