from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class MaterialCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    sku: str = Field(..., min_length=2, max_length=30)
    nome: str = Field(..., min_length=2, max_length=150)
    categoria_id: int = Field(..., gt=0)
    unidade_medida: str = Field(..., min_length=1, max_length=20)
    estoque_minimo: int = Field(default=0, ge=0)


class MaterialUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    sku: str = Field(..., min_length=2, max_length=30)
    nome: str = Field(..., min_length=2, max_length=150)
    categoria_id: int = Field(..., gt=0)
    unidade_medida: str = Field(..., min_length=1, max_length=20)
    estoque_minimo: int = Field(default=0, ge=0)


class MaterialResponse(BaseModel):
    id: int
    sku: str
    nome: str
    categoria_id: int
    unidade_medida: str
    saldo_atual: int
    estoque_minimo: int
    ativo: bool
    criado_em: datetime