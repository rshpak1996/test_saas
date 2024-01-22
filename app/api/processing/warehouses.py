from fastapi import HTTPException
from database import psql
import app.api.models.warehouses as ware_mod
import app.api.processing.parametr_sql_validator as psv


def get_warehouses(warehouse_id: int = None) -> dict:
    sql = f"""
    SELECT
    warehouses.id as warehouse_id,
    warehouses.title,
    warehouses.user_id,
    integrations.title AS integration_title,
    warehouse_statuses.title AS status_title
    
    FROM public.warehouses
    
    JOIN integrations ON warehouses.integration_id = integrations.integration_id
    JOIN warehouse_statuses ON warehouses.status_id = warehouse_statuses.status_id
    """

    if warehouse_id:
        sql += f"""
        WHERE warehouses.id = {warehouse_id}
        """
    try:
        data = {"data": psql.sql_fetchall(sql)}
    except Exception as e:
        print(e)
        data = {"data": []}
    return data


def delete_warehouse(warehouse_id: int):
    sql = f"""
    DELETE FROM public.warehouses
    WHERE id = {warehouse_id}
    RETURNING *
    """

    try:
        psql.sql_fetchall(sql)[0]
    except:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    raise HTTPException(status_code=200, detail="Warehouse deleted")


def create_warehouse(
        # TODO: missed integration_id
        data: ware_mod.WarehouseBase
) -> dict:
    if not data.title or not psv.is_valid_sql(data.title):
        raise HTTPException(status_code=404, detail="Invalid parameter")

    sql = sql = f"""
    
    with created_warehouse as (
        INSERT INTO public.warehouses(title, user_id, integration_id, status_id)
        VALUES (
            '{data.title}',
            {data.user_id},
            {data.integration_id},
            1
            )
        RETURNING warehouses.id,
        warehouses.title,
        warehouses.user_id,
        warehouses.integration_id,
        warehouses.status_id
        )
        
        SELECT 
        created_warehouse.id AS warehouse_id,
        created_warehouse.title,
        created_warehouse.user_id,
        integrations.title AS integration_title,
        warehouse_statuses.title AS status_title
        FROM created_warehouse
        JOIN integrations ON created_warehouse.integration_id = integrations.integration_id
        JOIN warehouse_statuses ON created_warehouse.status_id = warehouse_statuses.status_id
    """

    try:
        resp = psql.sql_fetchall(sql)[0]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=409, detail="Warehouse already exists")  # TODO: why 409?
    return resp
