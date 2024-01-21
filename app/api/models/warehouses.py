from enum import Enum
from pydantic import BaseModel, Field
from typing import List
import app.api.models.standard as standard


warehouse_id_description = "Onlihub unique warehouse id"
title_description = "Title of your warehouse"
user_id_description = "Onlihub unique user id"


class WarehouseStatuses(str, Enum):
    """
    <br>
    Current Warehouse status on Onlihub
    <br>
    <br>
    <b><i>Active:</i></b> This status indicates that the Warehouse is active and ready to receive updates.
    <br>
    <b><i>NotActive:</i></b> When a Warehouse is not active, it will not receive updates.
    """
    active = 'Active'
    not_active = 'NotActive'


class WarehouseResponse(BaseModel):
    id: int = Field(..., description=warehouse_id_description)
    title: str = Field(..., description=title_description)
    user_id: int = Field(..., description=user_id_description)
    integration_title: str = Field(...)
    warehouse_status_title: str = Field(...)


class Warehouses(BaseModel):
    data: List[WarehouseResponse]


class DetailsResponse(BaseModel):
    detail: str


response_example_warehouse = WarehouseResponse(
            id=111222,
            title="Warehouse 1",
            user_id=333444,
            integration_title='Integration 1',
            warehouse_status_title=WarehouseStatuses.active
        )


response_example_warehouses = Warehouses(
    data=[
        WarehouseResponse(
            id=111222,
            title="Warehouse 1",
            user_id=333444,
            integration_title='Integration 1',
            warehouse_status_title=WarehouseStatuses.active
        ),
        WarehouseResponse(
            id=111223,
            title="Warehouse 2",
            user_id=333445,
            integration_title='Integration 2',
            warehouse_status_title=WarehouseStatuses.not_active
        ),
    ]
)


common_responses_dell = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {"detail": "Warehouse has been deleted"}
            }
        }},
    400: standard.bad_request,
    401: standard.auth_error,
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Warehouse was not found"
                }
            }
        }
    }
}


# Создаем общие примеры ответов, используя type_responses
common_responses_one = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": dict(response_example_warehouse)
            }
        }},
    400: standard.bad_request,
    401: standard.auth_error,
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Warehouses was not found"
                }
            }
        }
    }
}

# Создаем общие примеры ответов, используя type_responses
common_responses_arr = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": dict(response_example_warehouses)
            }
        }
    },
    400: standard.bad_request,
    401: standard.auth_error
}