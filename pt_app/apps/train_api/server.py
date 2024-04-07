import os

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from apps.train_api.src.routers import train_router

app = FastAPI(redoc_url=None)

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


if __name__ == '__main__':
    uvicorn.run(app=app, host=os.environ.get('TRAIN_API_HOST'), port=int(os.environ.get('TRAIN_API_PORT')))