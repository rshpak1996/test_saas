from pydantic import BaseModel


class Details(BaseModel):
    message: str = None
    detail: str = None
    parameter: str = None


class StandardResponse(BaseModel):
    Err: Details = None


details_example_ok = Details(
    message='Unsuccessful',
    detail='Request processed unsuccessful',
    parameter='Get listings'
)

details_example_err = Details(
    message='successfully',
    detail='Request processed successfully',
    parameter='Get listings'
)

request_example_ok = StandardResponse(
    Err=details_example_ok
)

request_example_err = StandardResponse(
    Err=details_example_err
)

auth_error = {
        "description": "Authorisation Error",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Authorization error"
                }
            }
        }
    }

bad_request = {
        "description": "bad request",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {"loc":
                            [
                                "query",
                                "param"
                            ], "msg": "string", "type": "string"}
                    ]
                }
            }
        }
    }

not_found = {
        "description": "Not Found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Search error"
                }
            }
        }
    }