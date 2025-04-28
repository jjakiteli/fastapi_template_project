from fastapi import HTTPException


class UserNotFound(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = "User not found"
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExists(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "User already exists"
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserIsBanned(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "User is banned"
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectUserPassword(HTTPException):
    def __init__(self):
        self.status_code = 401
        self.detail = "Incorrect username or password"
        self.headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(
            status_code=self.status_code, detail=self.detail, headers=self.headers
        )
