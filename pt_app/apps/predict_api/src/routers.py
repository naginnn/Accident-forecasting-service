import io

from fastapi import APIRouter
from apps.predict_api.src.utils import get_recommendations
from starlette.responses import StreamingResponse

from src.reports.objects import create_objects_report, create_object_report, create_consumer_station_report

predict_router = APIRouter(
    tags=["predict"],
    prefix="/api/v1/predict",
    responses=None,
)


@predict_router.get("/", status_code=200)
async def predict_model(fields: str, model_name: str = 'default') -> list[dict]:
    rec = await get_recommendations(fields, model_name)
    return rec


@predict_router.get("/objects_report", status_code=200)
async def get_objects_report():
    file_name, excel_file = await create_objects_report()
    headers = {
        'Pragma': 'public',
        'Expires': '0',
        'Cache-Control': 'private',
        'Content-Disposition': f'attachment; filename="{file_name}.xlsx"',
        'Content-Transfer-Encoding': 'binary',
        'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }
    return StreamingResponse(content=io.BytesIO(excel_file), headers=headers)


@predict_router.get("/con_station_report/{id}", status_code=200)
async def get_consumer_station_report(id: int):
    file_name, excel_file = await create_consumer_station_report(id)
    headers = {
        'Pragma': 'public',
        'Expires': '0',
        'Cache-Control': 'private',
        'Content-Disposition': f'attachment; filename="{file_name}.xlsx"',
        'Content-Transfer-Encoding': 'binary',
        'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }
    return StreamingResponse(content=io.BytesIO(excel_file), headers=headers)


@predict_router.get("/objects_report/{id}", status_code=200)
async def get_object_report(id: int):
    file_name, excel_file = await create_object_report(id)
    headers = {
        'Pragma': 'public',
        'Expires': '0',
        'Cache-Control': 'private',
        'Content-Disposition': f'attachment; filename="{file_name}.xlsx"',
        'Content-Transfer-Encoding': 'binary',
        'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }
    return StreamingResponse(content=io.BytesIO(excel_file), headers=headers)
