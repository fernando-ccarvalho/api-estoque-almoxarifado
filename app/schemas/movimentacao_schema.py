from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

TipoMovimentacao = Literal["ENTRADA", "SAIDA"]


class MovimentacaoCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    material_id: int = Field(..., gt=0)
    tipo: TipoMovimentacao
    quantidade: int = Field(..., gt=0)
    observacao: str | None = Field(default=None, max_length=500)


class MovimentacaoResponse(BaseModel):
    id: int
    material_id: int
    tipo: TipoMovimentacao
    quantidade: int
    observacao: str | None
    data_movimentacao: datetime