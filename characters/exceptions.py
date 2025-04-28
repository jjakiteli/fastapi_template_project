from fastapi import HTTPException


class CharacterNotFound(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Character not found"
        super().__init__(status_code=self.status_code, detail=self.detail)


class CharacterAlreadyExists(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "Character already exists"
        super().__init__(status_code=self.status_code, detail=self.detail)
