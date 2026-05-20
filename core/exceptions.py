from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime



def error_response(status: int, error: str, request: Request):
    return JSONResponse(
        status_code=status,
        content={
            "status": status,
            "error": error,
            "path": str(request.url),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )

async def bad_request_handler(request: Request, exc):
    return error_response(400, str(exc.detail), request)


async def not_found_handler(request: Request, exc):
    return error_response(404, str(exc.detail), request)


async def server_error_handler(request: Request, exc):
    return error_response(500, "Internal server error", request)


async def unprocessable_handler(request: Request, exc):
    return error_response(422, "Validation error", request)


def register_exception_handlers(app):
    app.add_exception_handler(400, bad_request_handler)
    app.add_exception_handler(404, not_found_handler)
    app.add_exception_handler(500, server_error_handler)
    app.add_exception_handler(422, unprocessable_handler)