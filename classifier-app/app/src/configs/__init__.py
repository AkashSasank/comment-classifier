from functools import lru_cache
from .base import Settings


@lru_cache()
def get_settings():
    """Get different settings object according to different values of
    environment variable `MODE`, and use cache to speed up the execution.

    Returns:
        object: The instance of the current used settings class.
    """
    base_settings = Settings()
    return base_settings
