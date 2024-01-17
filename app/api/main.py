# -*- coding: utf-8 -*-
from fastapi import FastAPI
from app.api.handlers import docs, webhooks
import uvicorn
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware


description = """
OnliHub API helps you do awesome stuff. 🚀

## Get Started

<b>Introduction</b>

Onlihub is a dropship platform which does process dropship transactions for SMBs online retailers and brands. <a href="https://onlihub.com/" target="_blank">Learn more</a> about us.
Here you will find our complete API reference, along with guides and examples to follow.

<b>API access</b>

Before you are able to interact with Onlihub’s API you must have a <a href="https://onlihub.com/developer/apply" target="_blank">developer account</a> with us. You may submit application for 
developer account <a href="https://onlihub.com/developer/apply" target="_blank">here</a>. Once your developer application is approved you will be able to get your Authorization token.

<b>Support</b>

If you have any questions, please contact our Support team at support@onlihub.com 

"""

# Тут описание всех тегов/групп по тегам нужно связывать методы
tags_metadata = [
    {
        "name": "Authorization",
        "description":
            "When make a call to Onlihub API you need to include an 'Authorization' header with a valid bearer token in all your requests." 
            "You may get your Bearer token in your <a href='https://developer.onlihub.com/'>developer account</a>. "
    },
    {
            "name": "Sessions",
            "description":
                "In order to redirect user to Onlihub catalog you need to get a unique web link."
                "<br>If you set up your subdomain in your developer account – then we will return a web link with your domain name. "
                "For instance: <b>catalog.yourdomain.com</b>."
                "<br>If you don’t set up your subdomain – we will return a web link to Onlihub domain. For instance: <b>yourname.onlihub.com</b>."
    },
    {
        "name": "Listings",
        "description":
            "Use the Listings Resource to retrieve Onlihub listings. "
            "You may use filters (parameters) to retrieve certain Onlihub listings which you need. "
    },
    {
            "name": "User listings",
            "description":
                "Users are able to add Onlihub listings to their saved list on Onlihub. In order to retrieve user’s listings you may use endpoint "
                "Get user listing and/or you may create a <a href='https://provider.onlihub.com/#tag/Webhooks/operation/r_create_webhook_webhooks_post'>webhook</a> with an event UserListChange."
    },
    {
        "name": "Categories",
        "description":
            "Each Onlihub listing has a category. Use Categories Resource to retrieve Onlihub categories and the category tree."
    },
    {
        "name": "Payments",
        "description": "Use Payments Resource to retrieve user’s payments (purchase orders), create a payment for Onlihub products or create" 
        "payment to reload Onlihub wallet balance. Once you Create payment, we will return a web link to Stripe checkout. All payments "
        "are processed through external Stripe checkout."
        "<br> When users sold the Onlihub product(s) on any sales channel they need to purchase product(s) on Onlihub. To do that you "
        "should use <a href='https://provider.onlihub.com/#tag/Payments/operation/r_get_listing_payments_post'>Create payment</a> with <b>OrderPayment</b> data in the body request. "
        "<br> When users want to reload their Onlihub wallet balance you should use <a href='https://provider.onlihub.com/#tag/Payments/operation/r_get_listing_payments_post'>Create payment</a> with <b>WalletReload</b> data in the body "
        "request."
    },
    {
        "name": "Orders",
        "description":
            "Use Orders Resource to retrieve user’s orders containing product(s) from Onlihub."
    },
    {
        "name": "Wallet",
        "description": "Use Wallet Resource to retrieve current user’s wallet balance on Onlihub and/or list of purchase orders which were paid by user’s "
                        "wallet balance."
    },
    {
        "name": "Webhooks",
        "description":
            "<b>Overview</b><br><br>"
            "Onlihub's webhooks can simplify your development by pushing a payload to your app whenever certain events occur." 
            "<br>"
            "You may subscribe to webhooks through our Webhooks API or through your <a href='https://developer.onlihub.com/'>developer account</a>."
            "<br>"
            "<br>"
            "The endpoint allows you to create a new webhook configuration to subscribe to events and have events sent to a target URL. "
            "<br>Use the Webhooks Resource to create, view or delete subscriptions for specific events."
            "<br>"
            "<br>"
            "<b>Topics</b>"
            '''<table>
                        <th>Topic</th>
                        <th>Description</th>
                    </tr>
                    <tr>
                        <td>UserListAdd</td>
                        <td>Sends new product in user’s saved list on Onlihub.</td>
                    </tr>
                    <tr>
                        <td>UserListDelete</td>
                        <td>Sends deleted product in user’s list on Onlihub.</td>
                    </tr>
                    <tr>
                        <td>UsersListingStockChange</td>
                        <td>Sends the changed stock level of product from the user’s saved list on Onlihub.</td>
                    </tr>
                    <tr>
                        <td>PaymentStatusChange</td>
                        <td>Sends the changed payment status.</td>
                    </tr>
                    <tr>
                        <td>UsersListingPriceChange</td>
                        <td>Sends the changed price of product from the user’s saved list on Onlihub.</td>
                    </tr>
                    <tr>
                        <td>ShipmentTrackingUpdate</td>
                        <td>Sends the tracking number for the purchased product on Onlihub.</td>
                    </tr>
                    <tr>
                        <td>WebhookStatusChange</td>
                        <td>Sends the changed webhook status.</td>
                    </tr>
                    <tr>
                        <td>WalletBalanceChange</td>
                        <td>Sends the changed user’s wallet balance on Onlihub.</td>
                    </tr>
                    <tr>
                        <td>UsersListingContentChange</td>
                        <td>Sends the changed content of product from the user’s saved list on Onlihub.</td>
                    </tr>
                    <tr>
                        <td>ListingStockChange</td>
                        <td>Sends the changed stock level of Onlihub listing.</td>
                    </tr>
                    <tr>
                        <td>ListingPriceChange</td>
                        <td>Sends the changed price of Onlihub listing.</td>
                    </tr>
                    <tr>
                        <td>ListingContentChange</td>
                        <td>Sends the changed content of Onlihub listing.</td>
                    </tr>
                </table>'''
    }
]


def get_application() -> FastAPI:
    application = FastAPI(
        docs_url=None,
        redoc_url=None,
        title="Onlihub Developer API",
        description=description,
        version="1.0.0",
        contact={
            "name": "Onlihub Inc. ",
            "url": "https://onlihub.com/contact-us",
            "email": "support@onlihub.com",
        },
        openapi_tags=tags_metadata,
    )
    # Подключаем все роутеры
    application.include_router(docs.router)
    application.include_router(webhooks.router)

    return application


app = get_application()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Разрешить передачу аутентификационных куки и заголовков
    allow_methods=["*"],  # Разрешить все HTTP-методы (GET, POST, PUT, DELETE и т. д.)
    allow_headers=["*"],  # Разрешить все заголовки
)


# Определяем функцию custom_openapi для настройки x-logo
def custom_openapi():
    openapi_schema = get_openapi(
        title="OnliHub",
        version="1.0.0",
        contact={
            "name": "Onlihub Inc. ",
            "url": "https://onlihub.com/contact-us",
            "email": "support@onlihub.com",
        },
        description=description,
        routes=app.routes,
        tags=tags_metadata
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://marketplace.onlihub.com/images/logo.svg"
    }
    return openapi_schema


# Применяем custom_openapi к app.openapi
# Временно скрываем изза конфликта с вебхуком
# app.openapi = custom_openapi


if __name__ == '__main__':
    uvicorn.run('main:app', port=8016)
