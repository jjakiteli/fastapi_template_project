from fastapi import HTTPException


class InsufficientPermissions(HTTPException):
    def __init__(self):
        self.status_code = 403
        self.detail = "Insufficient permissions"
        super().__init__(status_code=self.status_code, detail=self.detail)


class RoleNotFound(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Role not found"
        super().__init__(status_code=self.status_code, detail=self.detail)


class RoleAlreadyExists(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "Role already exists"
        super().__init__(status_code=self.status_code, detail=self.detail)
