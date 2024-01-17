from fastapi.security import HTTPBearer
from pydantic import BaseModel
from fastapi import Depends, HTTPException
import database.onlihub_objects as onlihub_objects
import uuid

# Создайте зависимость для аутентификации по токену
http_bearer = HTTPBearer(
    scheme_name="Bearer Token",
    description="Bearer Token is a standard HTTP header used for authentication. "
                "To use it, include 'Authorization: Bearer <token>' in your request headers."
)


def is_valid_uuid(value):
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


# Модель для данных пользователя
class Integration(BaseModel):
    id: int
    title: str


# Функция для верификации токена одщего маркетплейса
def verify_token(token: HTTPBearer() = Depends(http_bearer)):
    if not is_valid_uuid(token.credentials):
        raise HTTPException(status_code=401, detail="Authorization error")
    integrations = onlihub_objects.onliub_object('integrations')
    integrations.getByFilter({"onlihub_token": token.credentials})
    if integrations.isEmpty():
        raise HTTPException(status_code=401, detail="Authorization error")
    else:
        return Integration(id=integrations.id, title=integrations.title)

