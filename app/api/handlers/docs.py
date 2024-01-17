from . import *

router = APIRouter()


# Делаем иконку
@router.get("/docs", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Onlihub API",
        swagger_favicon_url="https://media.onlihub.com/labels/Onlihub-favikon.png"
        )


@router.get("/redoc", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="Onlihub API",
        redoc_favicon_url="https://media.onlihub.com/labels/Onlihub-favikon.png"
    )


@router.get("/", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="Onlihub API",
        redoc_favicon_url="https://media.onlihub.com/labels/Onlihub-favikon.png"
    )