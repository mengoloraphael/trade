"""FastAPI dependencies"""

from fastapi import Depends, HTTPException, status
from functools import lru_cache
from src.config import get_settings


@lru_cache()
def get_settings_dependency():
    """Get settings"""
    return get_settings()


def verify_demo_mode(settings=Depends(get_settings_dependency)):
    """Verify that demo mode is enabled for write operations"""
    if not settings.demo_mode:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not allowed in production mode"
        )
