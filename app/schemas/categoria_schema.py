from typing import Annotated 
from pydantic import BaseModel, Field, ConfigDict

class CategoriaCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: str | None = Field(default=None, max_length=500)

class CategoriaResponse(BaseModel):
    id: int
    nome: str
    descricao: str | None

class CategoriaCreateLote(BaseModel):
    categorias: list[CategoriaCreate] = Field(..., min_length=1, max_length=100)


class CategoriaDeleteLote(BaseModel):
    ids: list[Annotated[int, Field(gt=0)]] = Field(..., min_length=1, max_length=100)


class CategoriaDeleteLoteResponse(BaseModel):
    ids_deletados: list[int]
    ids_nao_encontrados: list[int]
    total_deletado: int