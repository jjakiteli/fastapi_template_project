from fastapi import HTTPException


class InvalidCredentials(HTTPException):
    def __init__(self):
        self.status_code = 401
        self.detail = "Could not validate credentials"
        self.headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(
            status_code=self.status_code, detail=self.detail, headers=self.headers
        )
