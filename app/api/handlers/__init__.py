from fastapi import Depends, APIRouter, HTTPException, Body
from fastapi.security import HTTPBearer
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from enum import Enum
from pydantic import BaseModel
from app.api.auth.auth_utils import verify_token