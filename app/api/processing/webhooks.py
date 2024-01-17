import database.psql as psql
import app.api.models.webhooks as mod_webhooks
from fastapi import HTTPException
import app.api.processing.parametr_sql_validator as psv


def get_type_id(topic=mod_webhooks.WebhookTopics):
    if not topic:
        return 0
    elif topic == mod_webhooks.WebhookTopics.listing_content_change:
        return 1
    elif topic == mod_webhooks.WebhookTopics.listing_price_change:
        return 2
    elif topic == mod_webhooks.WebhookTopics.listing_stock_change:
        return 3
    elif topic == mod_webhooks.WebhookTopics.shipment_tracking_update:
        return 4
    elif topic == mod_webhooks.WebhookTopics.wallet_balance_change:
        return 5
    elif topic == mod_webhooks.WebhookTopics.payment_status_change:
        return 6
    elif topic == mod_webhooks.WebhookTopics.webhook_status_change:
        return 7
    elif topic == mod_webhooks.WebhookTopics.user_list_add:
        return 8
    elif topic == mod_webhooks.WebhookTopics.users_listing_stock_change:
        return 9
    elif topic == mod_webhooks.WebhookTopics.users_listing_price_change:
        return 10
    elif topic == mod_webhooks.WebhookTopics.users_listing_content_change:
        return 11
    elif topic == mod_webhooks.WebhookTopics.user_list_delete:
        return 12
    else:
        return 0


id_to_topic = {
    1: mod_webhooks.WebhookTopics.listing_content_change,
    2: mod_webhooks.WebhookTopics.listing_price_change,
    3: mod_webhooks.WebhookTopics.listing_stock_change,
    4: mod_webhooks.WebhookTopics.shipment_tracking_update,
    5: mod_webhooks.WebhookTopics.wallet_balance_change,
    6: mod_webhooks.WebhookTopics.payment_status_change,
    7: mod_webhooks.WebhookTopics.webhook_status_change,
    8: mod_webhooks.WebhookTopics.user_list_add,
    9: mod_webhooks.WebhookTopics.users_listing_stock_change,
    10: mod_webhooks.WebhookTopics.users_listing_price_change,
    11: mod_webhooks.WebhookTopics.users_listing_content_change,
    12: mod_webhooks.WebhookTopics.user_list_delete
}


def get_webhooks(integration_id: int, webhook_id: int = None) -> dict:
    sql = f"""SELECT 
        integration_webhooks.id AS webhook_id,
        integration_webhooks.description,
        integration_webhooks.url,
        integration_webhooks.webhook_secret_key,
        CASE WHEN integration_webhooks.status_id = 1 THEN 'Active' ELSE 'NotActive' END AS status,
        array_agg(webhook_topic_types.title) AS topics
        FROM public.integration_webhooks
        LEFT JOIN public.webhook_topics ON webhook_topics.webhook_id = integration_webhooks.id
        LEFT JOIN public.webhook_topic_types ON webhook_topic_types.id = webhook_topics.webhook_topic_type_id
        WHERE integration_id ={integration_id} """
    if webhook_id:
        sql += f"AND integration_webhooks.id = {webhook_id}"

    sql += " GROUP BY integration_webhooks.id"
    try:
        data = {"data": psql.sql_fetchall(sql)}
    except Exception as e:
        print(e)
        data = {"data": []}
    return data


def create_webhook(integration_id, data: mod_webhooks.WebhookBase) -> dict:
    if (data.description and not psv.is_valid_sql(data.description)) or not psv.is_valid_sql(data.url):
        raise HTTPException(status_code=404, detail="Invalid parameter")

    sql = f'''INSERT INTO public.integration_webhooks (description, url, integration_id, webhook_secret_key, status_id)
        VALUES (
            '{data.description}',  -- Замените на нужный заголовок
            '{data.url}',  -- Замените на нужный URI
            {integration_id},  -- Значение ID интеграции
            uuid_generate_v4(),
            1
        )
        ON CONFLICT (integration_id, url) DO NOTHING
        RETURNING integration_webhooks.id AS webhook_id,
        integration_webhooks.description,
        integration_webhooks.url,
        integration_webhooks.webhook_secret_key,
        CASE WHEN integration_webhooks.status_id = 1 THEN 'Active' ELSE 'NotActive' END AS status
        '''

    try:
        resp = psql.sql_fetchall(sql)[0]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=409, detail="Webhook already exists")

    # Создайте записи о событиях в таблице webhook_topics
    webhook_id = resp["webhook_id"]
    topic_values = ", ".join([f'({webhook_id}, {get_type_id(topic)})' for topic in data.topics])
    if topic_values:
        create_topics_sql = f'''INSERT INTO public.webhook_topics (webhook_id, webhook_topic_type_id)
                VALUES {topic_values} ON CONFLICT (webhook_id, webhook_topic_type_id) DO NOTHING RETURNING webhook_topics.webhook_id AS id;
            '''
        try:
            psql.sql_fetchall(create_topics_sql)
            resp.topics = data.topics
        except:
            HTTPException(status_code=400, detail="Failed to add topics")

    return resp


def update_webhook(integration_id, webhook_id: int, data: mod_webhooks.WebhookPut) -> dict:
    if (data.description and not psv.is_valid_sql(data.description)) or not psv.is_valid_sql(data.url):
        raise HTTPException(status_code=404, detail="Invalid parameter")

    set_text = ''
    if data.description and psv.is_valid_sql(data.description):
        set_text += f"description = '{data.description}',"
    if data.url and psv.is_valid_sql(data.url):
        set_text += f"url = '{data.url}',"
    if data.status:
        if data.status == mod_webhooks.WebhookStatuses.active:
            set_text += f'status_id = 1,'
        else:
            set_text += f'status_id = 2,'
    sql = f'''UPDATE public.integration_webhooks
        SET 
            {set_text}
            updated_at = now()
        WHERE 
            integration_id = {integration_id}  -- Значение ID интеграции
            AND id = {webhook_id} 
        RETURNING 
        integration_webhooks.id AS webhook_id,
        integration_webhooks.description,
        integration_webhooks.url,
        integration_webhooks.webhook_secret_key,
        CASE WHEN integration_webhooks.status_id = 1 THEN 'Active' ELSE 'NotActive' END AS status
        '''

    try:
        resp = psql.sql_fetchall(sql)[0]
        resp.topics = []
    except Exception as e:
        if 'duplicate key value' in str(e):
            raise HTTPException(status_code=404, detail="url is already used in another webhook")
        else:
            raise HTTPException(status_code=404, detail="Webhook not found")

    if data.topics and len(data.topics):
        # Сначала удаляем существующие события для этого вебхука
        delete_topics_sql = f'''DELETE FROM public.webhook_topics WHERE webhook_id = {webhook_id}'''
        try:
            del_resp = psql.sql_fetchall(delete_topics_sql)
        except:
            pass

        for topic in data.topics:
            create_topic_sql = f'''INSERT INTO public.webhook_topics (webhook_id, webhook_topic_type_id)
                    VALUES ({webhook_id}, {get_type_id(topic)}) RETURNING webhook_id AS id;
                '''
            try:
                psql.sql_fetchall(create_topic_sql)
            except Exception as e:
                print(e)
                pass

        resp.topics = data.topics
    else:
        # Получаем текущие ивенты
        sql = f'''SELECT webhook_topic_types.title FROM public.webhook_topics
            JOIN public.webhook_topic_types ON webhook_topic_types.id = webhook_topics.webhook_topic_type_id
            WHERE webhook_topics.webhook_id = {webhook_id} 
        '''
        resp_ev = psql.sql_fetchall(sql)
        for topic in resp_ev:
            resp.topics.append(topic.title)

    return resp


def delete_webhook(integration_id, webhook_id: int):
    sql = f'''DELETE FROM public.integration_webhooks
    WHERE id = {webhook_id}  -- Значение ID вебхука
    AND integration_id = {integration_id} RETURNING *'''

    try:
        psql.sql_fetchall(sql)[0]
    except:
        raise HTTPException(status_code=404, detail="Webhook not found")
    raise HTTPException(status_code=200, detail="Webhook deleted")


if __name__ == "__main__":
    get_webhooks(16)