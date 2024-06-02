import os

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from pt_app.apps.predict_api.src.routers import predict_router
app = FastAPI(
    redoc_url=None
)

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

app.include_router(predict_router)


if __name__ == '__main__':
    uvicorn.run(app=app, host=os.environ.get('PREDICT_API_HOST'), port=int(os.environ.get('PREDICT_API_PORT')))