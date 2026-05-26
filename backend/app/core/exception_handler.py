from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from app.models.common import ApiResponse


async def http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail
    if isinstance(detail, dict):
        return JSONResponse(
            status_code=exc.status_code,
            content=ApiResponse(
                code=exc.status_code,
                data=detail,
                msg=detail.get("message", ""),
            ).model_dump(),
        )
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse(
            code=exc.status_code,
            data=None,
            msg=str(detail),
        ).model_dump(),
    )


async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ApiResponse(code=500, data=None, msg="服务器内部错误").model_dump(),
    )
