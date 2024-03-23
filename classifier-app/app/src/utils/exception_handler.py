import traceback

from fastapi import status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from .logger import logger


class ExceptionHandler:
    """
    Class to define exception handler
    """

    @staticmethod
    async def handler(request, exc):
        """
        Handles exceptions and returns JSON response based on exception type
        :param request:
        :param exc:
        :return:
        """
        logger.exception(traceback.format_exc())
        logger.exception(exc)
        if isinstance(exc, HTTPException):
            return JSONResponse(
                content=exc.detail,
                status_code=exc.status_code
            )
        return JSONResponse(
            content={
                "message": "Something went wrong"
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
