"""Module containing FastAPI instance related functions and classes."""
# mypy: ignore-errors
import logging.config
from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from .api import api_router
from .version import __version__
from .configs import get_settings
from .events import (
    startup_handler, shutdown_handler
)
from .utils.exception_handler import ExceptionHandler


def create_application() -> FastAPI:
    """Create a FastAPI instance.

    Returns:
        object of FastAPI: the fastapi application instance.
    """
    settings = get_settings()
    application = FastAPI(title=settings.PROJECT_NAME,
                          debug=settings.DEBUG,
                          version=__version__,
                          openapi_url=f"{settings.API_STR}/openapi.json")

    # Allow cors
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # add defined routers
    application.include_router(api_router, prefix=settings.API_STR)

    # event handler
    application.add_event_handler("startup", startup_handler)
    application.add_event_handler("shutdown", shutdown_handler)

    #  exception handler
    application.add_exception_handler(handler=ExceptionHandler.handler,
                                      exc_class_or_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # load logging config
    logging.config.dictConfig(settings.LOGGING_CONFIG)

    return application
