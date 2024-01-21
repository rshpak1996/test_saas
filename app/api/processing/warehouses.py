from database import psql


def get_warehouses(warehouse_id: int = None) -> dict:
    sql = f"""
    SELECT
    warehouses.id,
    warehouses.title,
    warehouses.user_id,
    integrations.title AS integration_title,
    warehouse_statuses.title AS warehouse_status_title
    
    FROM warehouses
    
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
