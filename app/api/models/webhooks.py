from pydantic import BaseModel, Field
from enum import Enum
from typing import List
import app.api.models.standard as standard


id_description = "Onlihub unique webhook id"
webhook_key_description = "Onlihub unique webhook key"
title_description = "Your internal title of what the webhook is used for"
url_description = "URL we will call when an event matching the subscription topic is raised"

webhook_events_description = """
<br>
    Topic of the webhook requested
    <br>
    <br>
    <b>UserListAdd:</b> Sends new product in user’s saved list on Onlihub.
    <br>
    <b>UserListDelete:</b> Sends deleted product in user’s list on Onlihub.
    <br>
    <b>UsersListingStockChange:</b> Sends the changed stock level of product from the user’s saved list on Onlihub.
    <br>
    <b>UsersListingPriceChange:</b> Sends the changed price of product from the user’s saved list on Onlihub
    <br>
    <b>UsersListingContentChange:</b> Sends the changed content of product from the user’s saved list on Onlihub.
    <br>
    <b>ListingContentChange:</b> Sends the changed content of Onlihub listing.
    <br>
    <b>ListingPriceChange:</b> Sends the changed price of Onlihub listing.
    <br>
    <b>ListingStockChange:</b> Sends the changed stock level of Onlihub listing.
    <br>
    <b>ShipmentTrackingUpdate:</b> Sends the tracking number for the purchased product on Onlihub.
    <br>
    <b>WalletBalanceChange:</b> Sends the changed user’s wallet balance on Onlihub.
    <br>
    <b>PaymentStatusChange:</b> Sends the changed payment status.
    <br>
    <b>WebhookStatusChange:</b> Subscribe to changes in webhook status.
"""


class WebhookTopics(str, Enum):
    listing_content_change = 'ListingContentChange'
    listing_price_change = 'ListingPriceChange'
    listing_stock_change = 'ListingStockChange'
    shipment_tracking_update = 'ShipmentTrackingUpdate'
    wallet_balance_change = 'WalletBalanceChange'
    payment_status_change = 'PaymentStatusChange'
    webhook_status_change = 'WebhookStatusChange'
    user_list_add = 'UserListAdd'
    user_list_delete = 'UserListDelete'
    users_listing_stock_change = 'UsersListingStockChange'
    users_listing_price_change = 'UsersListingPriceChange'
    users_listing_content_change = 'UsersListingContentChange'


class WebhookStatuses(str, Enum):
    """
    <br>
    Current webhook status on Onlihub
    <br>
    <br>
    <b><i>Active:</i></b> This status indicates that the webhook is active and ready to receive updates.
    <br>
    <b><i>NotActive:</i></b> When a webhook is not active, it will not receive updates.
    """
    active = 'Active'
    not_active = 'NotActive'


class WebhookBase(BaseModel):
    description: str = Field(default=None, description=title_description)
    url: str = Field(..., description=url_description)
    topics: List[WebhookTopics] = Field(..., description=webhook_events_description)


class WebhookPut(BaseModel):
    description: str = Field(default=None, description=title_description)
    url: str = Field(None, description=url_description)
    topics: List[WebhookTopics] = Field(None, description=webhook_events_description)
    status: WebhookStatuses = None


class WebhookResponse(BaseModel):
    webhook_id: int = Field(..., description=id_description)
    webhook_secret_key: str = Field(..., description=webhook_key_description)
    description: str = Field(..., description=title_description)
    url: str = Field(..., description=url_description)
    topics: List[WebhookTopics] = Field(..., description=webhook_events_description)
    status: WebhookStatuses


class Webhooks(BaseModel):
    data: List[WebhookResponse]


class DetailsResponse(BaseModel):
    detail: str


request_example_one = WebhookBase(
    description="Webhook 1",
    url="https://example.com/webhook",
    topics=[WebhookTopics.shipment_tracking_update],
)


response_example_webhook = WebhookResponse(
            webhook_id=111222,
            description="Webhook 1",
            url="https://example.com/webhook",
            topics=[WebhookTopics.listing_stock_change],
            status=WebhookStatuses.active,
            webhook_secret_key='sdfsdferwvfvi3428efhusdyhf873h4'
)


response_example_webhooks = Webhooks(
    data=[
        WebhookResponse(
            webhook_id=111222,
            description="Webhook 1",
            url="https://example.com/webhook",
            topics=[WebhookTopics.listing_stock_change],
            status=WebhookStatuses.active,
            webhook_secret_key='sdfsdferwvfvi3428efhusdyhf873h4'
        ),
        WebhookResponse(
            webhook_id=111223,
            description="Webhook 2",
            url="https://example.com/webhook",
            topics=[WebhookTopics.shipment_tracking_update],
            status=WebhookStatuses.active,
            webhook_secret_key='sdfsdferwvfvi3428efhusdyhf873h5'
        )
    ]
)


common_responses_dell = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {"detail": "Webhook has been deleted"}
            }
        }},
    400: standard.bad_request,
    401: standard.auth_error,
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Webhook was not found"
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
                "example": dict(response_example_webhook)
            }
        }},
    400: standard.bad_request,
    401: standard.auth_error,
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Webhook was not found"
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
                "example": dict(response_example_webhooks)
            }
        }
    },
    400: standard.bad_request,
    401: standard.auth_error
}
