from . import *
from fastapi import APIRouter
import app.api.models.warehouses as ware_mod
import app.api.processing.warehouses as ware_proc
from fastapi import Path

router = APIRouter()


@router.get(
    "/warehouses",
    response_model=ware_mod.Warehouses,
    responses=ware_mod.common_responses_arr,
    summary="Get warehouses",
    description="Display a list of all warehouses with information",
    tags=['Warehouses'],
    operation_id="get_warehouses"
)
def r_get_warehouses():
    return ware_proc.get_warehouses()


@router.get(
    "/warehouses/{warehouses_id}",
    response_model=ware_mod.WarehouseResponse,
    responses=ware_mod.common_responses_one,
    summary="Get warehouse",
    description="Display information of one selected warehouse",
    tags=['Warehouses'],
    operation_id="get_warehouse"
)
def r_get_warehouse(warehouses_id):
    whs = ware_proc.get_warehouses(warehouse_id=warehouses_id)
    item = whs.get('data', [])
    if not item:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return item[0]


@router.delete(
    "/warehouses/{warehouses_id}",
    response_model=ware_mod.DetailsResponse,
    responses=ware_mod.common_responses_dell,
    summary="Delete an existing warehouse",
    description="Delete a single warehouse specified by the warehouse ID in the path.",
    tags=['Warehouses'],
    operation_id="delete_warehouse"
)
def r_delete_warehouse(
    warehouses_id: int = Path(..., title="Warehouse ID", description=ware_mod.warehouse_id_description),
):
    ware_proc.delete_warehouse(warehouses_id)
