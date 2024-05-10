import os

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from apps.train_api.service.training_test import prepare_dataset
from apps.train_api.src.routers import train_router
from fastapi.openapi.docs import (
    get_swagger_ui_html,
)
from fastapi.openapi.utils import get_openapi
# app = FastAPI(redoc_url=None)
app = FastAPI(docs_url=None,
              redoc_url=None,
              openapi_url="/docs/train/openapi.json")
static_path = "/".join(os.getcwd().split('/')[:len(os.getcwd().split('/'))-2])
if static_path == '':
    static_path = os.getcwd()
app.mount(static_path, StaticFiles(directory=static_path), name="static")

""" Настройки CORS """

origins = [
    "*",
]

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(train_router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="S3 REPL service",
        version="1.0.0",
        description="replication service",
        routes=app.routes,
    )
    # openapi_schema["info"]["x-logo"] = {
    #     "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    # }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/docs/train", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        # openapi_url="/url_root/openapi.json",
        title="App1 api",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url=f"{static_path}/static/swagger/swagger-ui-bundle.js",  # Optional
        swagger_css_url=f"{static_path}/static/swagger/swagger-ui.css",  # Optional
        # swagger_favicon_url="/static/swagger/favicon-32x32.png",  # Optional
        swagger_favicon_url=f"{static_path}/static/swagger/innovation.png",  # Optional
        # custom_js_url="/static/custom_script.js",
    )

if __name__ == '__main__':
    import pandas as pd
    files = {}
    files["test.xlsx"] = pd.ExcelFile(f"{os.getcwd()}/autostart/test.xlsx", )
    prepare_dataset(files=files)
    uvicorn.run(app=app, host=os.environ.get('TRAIN_API_HOST'), port=int(os.environ.get('TRAIN_API_PORT')))