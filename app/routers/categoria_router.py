from typing import Annotated

from fastapi import APIRouter, Path, status

from app.schemas.categoria_schema import (
    CategoriaCreate,
    CategoriaCreateLote,
    CategoriaDeleteLote,
    CategoriaDeleteLoteResponse,
    CategoriaResponse,
)
from app.services import categoria_service

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.post(
    "/",
    response_model=CategoriaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_categoria(dados: CategoriaCreate):
    return categoria_service.criar_categoria(dados)


@router.post(
    "/lote",
    response_model=list[CategoriaResponse],
    status_code=status.HTTP_201_CREATED,
)
def criar_categorias_em_lote(dados: CategoriaCreateLote):
    return categoria_service.criar_categorias_em_lote(dados)


@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias():
    return categoria_service.listar_categorias()


@router.get("/{categoria_id}", response_model=CategoriaResponse)
def buscar_categoria_por_id(categoria_id: Annotated[int, Path(gt=0)]):
    return categoria_service.buscar_categoria_por_id(categoria_id)


@router.put("/{categoria_id}", response_model=CategoriaResponse)
def atualizar_categoria(
    categoria_id: Annotated[int, Path(gt=0)],
    dados: CategoriaCreate,
):
    return categoria_service.atualizar_categoria(categoria_id, dados)


@router.delete("/lote", response_model=CategoriaDeleteLoteResponse)
def deletar_categorias_em_lote(dados: CategoriaDeleteLote):
    return categoria_service.deletar_categorias_em_lote(dados)


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_categoria(categoria_id: Annotated[int, Path(gt=0)]):
    categoria_service.deletar_categoria(categoria_id)