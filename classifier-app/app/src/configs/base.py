from typing import Dict
from pydantic import BaseModel, AnyHttpUrl, BaseSettings, validator, PostgresDsn


class LoggingConfig(BaseModel):
    version: int
    disable_existing_loggers: bool = False
    formatters: Dict
    handlers: Dict
    loggers: Dict


class Settings(BaseSettings):
    PROJECT_NAME: str = 'Classifier APP'
    PROJECT_SLUG: str = 'classifier-app'

    DEBUG: bool = True
    API_STR: str = "/api/v1"

    # ######################## Logging Configuration ###########################
    LOGGING_CONFIG: LoggingConfig = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
        },
        "handlers": {
            'consoleHandler': {
                'class': 'logging.StreamHandler',
                'level': "DEBUG",
            },
        },
        "loggers": {
            "feddit": {
                'handlers': ['consoleHandler'],
                'level': "DEBUG",
            },
            "uvicorn": {
                'handlers': ['consoleHandler']
            },
            "uvicorn.access": {
                # Use the project logger to replace uvicorn.access logger
                'handlers': []
            }
        }
    }

    class Config:
        case_sensitive = True
