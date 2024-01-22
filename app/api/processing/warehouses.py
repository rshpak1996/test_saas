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


def create_warehouse(data: ware_mod.WarehouseBase) -> dict:  # TODO: missed integration_id
    if not data.title or not psv.is_valid_sql(data.title):
        raise HTTPException(status_code=404, detail="Invalid parameter")

    sql = f"""
    
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


def update_warehouses(warehouse_id: int, data: ware_mod.WarehousePut) -> dict:
    if not data.title or not psv.is_valid_sql(data.title):
        raise HTTPException(status_code=404, detail="Invalid parameter")

    set_text = ''
    if data.title and psv.is_valid_sql(data.title):
        set_text += f"title = '{data.title}',"
    if data.user_id:
        set_text += f"user_id = {data.user_id},"
    if data.integration_id:
        set_text += f"integration_id = {data.integration_id},"

    if data.status_title:
        if data.status_title == ware_mod.WarehouseStatuses.active:
            set_text += f'status_id = 1'
        else:
            set_text += f'status_id = 2'

    if not set_text:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    sql = f'''
       WITH updated_warehouse AS (
           UPDATE public.warehouses
           SET {set_text}
           WHERE id = {warehouse_id}
           RETURNING id, title, user_id, integration_id, status_id
       )

       SELECT 
           updated_warehouse.id AS warehouse_id,
           updated_warehouse.title,
           updated_warehouse.user_id,
           integrations.title AS integration_title,
           warehouse_statuses.title AS status_title
       FROM updated_warehouse
       JOIN integrations ON updated_warehouse.integration_id = integrations.integration_id
       JOIN warehouse_statuses ON updated_warehouse.status_id = warehouse_statuses.status_id
       '''

    try:
        resp = psql.sql_fetchall(sql)[0]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Warehouse not found")
    return resp
