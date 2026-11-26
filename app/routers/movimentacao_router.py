from typing import Annotated

from fastapi import APIRouter, Path, Query, status

from app.schemas.movimentacao_schema import (
    MovimentacaoCreate,
    MovimentacaoResponse,
    TipoMovimentacao,
)
from app.services import movimentacao_service

router = APIRouter(prefix="/movimentacoes", tags=["Movimentações"])


@router.post(
    "/",
    response_model=MovimentacaoResponse,
    status_code=status.HTTP_201_CREATED,
)
def registrar_movimentacao(dados: MovimentacaoCreate):
    return movimentacao_service.registrar_movimentacao(dados)


@router.get("/", response_model=list[MovimentacaoResponse])
def listar_movimentacoes(
    material_id: Annotated[int | None, Query(gt=0)] = None,
    tipo: Annotated[TipoMovimentacao | None, Query()] = None,
):
    return movimentacao_service.listar_movimentacoes(
        material_id=material_id,
        tipo=tipo,
    )


@router.get("/{movimentacao_id}", response_model=MovimentacaoResponse)
def buscar_movimentacao_por_id(movimentacao_id: Annotated[int, Path(gt=0)]):
    return movimentacao_service.buscar_movimentacao_por_id(movimentacao_id)