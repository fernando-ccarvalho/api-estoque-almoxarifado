from typing import Annotated

from fastapi import APIRouter, Path, Query, status

from app.schemas.material_schema import (
    MaterialCreate,
    MaterialResponse,
    MaterialUpdate,
)
from app.services import material_service

router = APIRouter(prefix="/materiais", tags=["Materiais"])


@router.post(
    "/",
    response_model=MaterialResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_material(dados: MaterialCreate):
    return material_service.criar_material(dados)


@router.get("/", response_model=list[MaterialResponse])
def listar_materiais(
    apenas_ativos: Annotated[bool, Query()] = True,
):
    return material_service.listar_materiais(apenas_ativos=apenas_ativos)


@router.get("/{material_id}", response_model=MaterialResponse)
def buscar_material_por_id(material_id: Annotated[int, Path(gt=0)]):
    return material_service.buscar_material_por_id(material_id)


@router.put("/{material_id}", response_model=MaterialResponse)
def atualizar_material(
    material_id: Annotated[int, Path(gt=0)],
    dados: MaterialUpdate,
):
    return material_service.atualizar_material(material_id, dados)


@router.delete("/{material_id}", response_model=MaterialResponse)
def inativar_material(material_id: Annotated[int, Path(gt=0)]):
    return material_service.inativar_material(material_id)