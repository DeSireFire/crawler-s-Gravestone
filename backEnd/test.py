import uvicorn
# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
#
#
# class UnicornException(Exception):
#     def __init__(self, name: str):
#         self.name = name
#
#
# app = FastAPI()
#
#
# @app.exception_handler(UnicornException)
# async def unicorn_exception_handler(request: Request, exc: UnicornException):
#     return JSONResponse(
#         status_code=418,
#         content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
#     )
#
#
# @app.get("/")
# async def read_unicorn(name: str):
#     if name == "yolo":
#         raise UnicornException(name=name)
#     return {"unicorn_name": name}
# if __name__ == "__main__":
#     uvicorn.run(app='test:app', port=8080)




# from fastapi import FastAPI
# from fastapi.middleware import Middleware
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.middleware.gzip import GZipMiddleware
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
# from fastapi.middleware.trustedhost import TrustedHostMiddleware
# from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
# from fastapi.openapi.utils import get_openapi
# from fastapi.responses import HTMLResponse
#
# app = FastAPI()
#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}
#
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
from apps.workerLogs.logClient import crawlLogUper

obj = crawlLogUper()
logger = obj.logger
logger.info(f'这是一条 信息 日志，发出来测试一下！！！ 我就是发出来测试一下')
del logger
