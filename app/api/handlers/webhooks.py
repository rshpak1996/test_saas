from . import *
import app.api.models.webhooks as hook_mod
import app.api.processing.webhooks as hook_proc
from fastapi import Path
from pydantic import BaseModel

router = APIRouter()


@router.get(
    "/webhooks",
    response_model=hook_mod.Webhooks,
    responses=hook_mod.common_responses_arr,
    summary="Get webhooks",
    description="This endpoint returns all webhook configurations associated with the current account as a paged result set.",
    openapi_extra='',
    tags=['Webhooks'],
    operation_id="get_webhooks"
)
def r_get_webhooks(integration: BaseModel = Depends(verify_token)):
    return hook_proc.get_webhooks(integration.id)


@router.get(
    "/webhooks/{webhook_id}",
    response_model=hook_mod.WebhookResponse,
    responses=hook_mod.common_responses_one,
    summary="Get webhook",
    description="This endpoint gets a single webhook configuration specified by the webhook ID in the path.",
    tags=['Webhooks'],
    operation_id="get_webhook"
)
def r_get_webhook(webhook_id: int, integration: BaseModel = Depends(verify_token)):
    whk = hook_proc.get_webhooks(integration.id, webhook_id)
    item = whk.get('data', [])
    if not item:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return item[0]


@router.post(
    "/webhooks",
    response_model=hook_mod.WebhookResponse,
    responses=hook_mod.common_responses_one,
    summary="Create a new webhook configuration",
    description="The endpoint allows you to create a new webhook configuration to subscribe to topics and have events sent to a target URL.",
    tags=['Webhooks'],
    operation_id="create_webhook"
)
def r_create_webhook(
        integration: BaseModel = Depends(verify_token),
        data: hook_mod.WebhookBase = Body(..., example=hook_mod.request_example_one)
):
    return hook_proc.create_webhook(integration.id, data)


@router.put(
    "/webhooks/{webhook_id}",
    response_model=hook_mod.WebhookResponse,
    responses=hook_mod.common_responses_one,
    summary="Update an existing webhook configuration",
    description="Updates the webhook configuration specified by the path with the request body.",
    tags=['Webhooks'],
    operation_id="update_webhook"
)
def r_update_webhook(
        webhook_id: int,
        integration: BaseModel = Depends(verify_token),
        data: hook_mod.WebhookPut = Body(..., example=hook_mod.request_example_one)
):
    return hook_proc.update_webhook(integration.id, webhook_id, data)


@router.delete(
    "/webhooks/{webhook_id}",
    response_model=hook_mod.DetailsResponse,
    responses=hook_mod.common_responses_dell,
    summary="Delete an existing webhook configuration",
    description="Delete a single webhook configuration specified by the webhook ID in the path.",
    tags=['Webhooks'],
    operation_id="delete_webhook"
)
def r_del_webhooks(
        webhook_id: int = Path(..., title="Webhook ID", description=hook_mod.id_description),
        integration: BaseModel = Depends(verify_token),
):
    hook_proc.delete_webhook(integration.id, webhook_id)