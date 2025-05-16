from fastapi.exceptions import HTTPException

class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Not Found", status_code: int = 404):
        super().__init__(status_code=status_code, detail=detail)