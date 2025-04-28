from fastapi import HTTPException


class UserNotBanned(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = "User not banned"
        super().__init__(status_code=self.status_code, detail=self.detail)
