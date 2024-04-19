from pydantic import BaseModel

class ConflictErrorSchema(BaseModel):
    message: str = "Já está cadastrado!"

class BadRequestErrorSchema(BaseModel):
    message: str = "Erro no formato da requisição!"