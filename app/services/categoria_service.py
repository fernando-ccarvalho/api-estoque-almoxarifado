from psycopg.errors import ForeignKeyViolation, UniqueViolation

from app.exceptions import ConflitoError, NaoEncontradoError
from app.repositories import categoria_repository
from app.schemas.categoria_schema import (
    CategoriaCreate,
    CategoriaCreateLote,
    CategoriaDeleteLote,
)


def criar_categoria(dados: CategoriaCreate):
    if categoria_repository.buscar_por_nome(dados.nome):
        raise ConflitoError(f"Já existe uma categoria com o nome '{dados.nome}'.")

    try:
        return categoria_repository.criar(dados.nome, dados.descricao)
    except UniqueViolation:
        raise ConflitoError(f"Já existe uma categoria com o nome '{dados.nome}'.")


def criar_categorias_em_lote(dados: CategoriaCreateLote):
    vistos = set()
    duplicados_no_lote = []

    for item in dados.categorias:
        chave = item.nome.lower()
        if chave in vistos:
            duplicados_no_lote.append(item.nome)
        vistos.add(chave)

    if duplicados_no_lote:
        nomes_str = ", ".join(duplicados_no_lote)
        raise ConflitoError(f"Nomes repetidos dentro do próprio lote: {nomes_str}.")

    nomes = [item.nome for item in dados.categorias]
    existentes = categoria_repository.buscar_por_nomes(nomes)

    if existentes:
        nomes_existentes = ", ".join(cat["nome"] for cat in existentes)
        raise ConflitoError(f"Categorias já cadastradas no banco: {nomes_existentes}.")

    lista_dicts = [item.model_dump() for item in dados.categorias]

    try:
        return categoria_repository.criar_em_lote(lista_dicts)
    except UniqueViolation:
        raise ConflitoError("Uma ou mais categorias do lote já foram cadastradas.")


def listar_categorias():
    return categoria_repository.listar_todas()


def buscar_categoria_por_id(categoria_id: int):
    categoria = categoria_repository.buscar_por_id(categoria_id)
    if not categoria:
        raise NaoEncontradoError(f"Categoria com id {categoria_id} não encontrada.")
    return categoria


def atualizar_categoria(categoria_id: int, dados: CategoriaCreate):
    categoria_atual = categoria_repository.buscar_por_id(categoria_id)
    if not categoria_atual:
        raise NaoEncontradoError(f"Categoria com id {categoria_id} não encontrada.")

    existente = categoria_repository.buscar_por_nome(dados.nome)
    if existente and existente["id"] != categoria_id:
        raise ConflitoError(f"Já existe outra categoria com o nome '{dados.nome}'.")

    try:
        atualizada = categoria_repository.atualizar(
            categoria_id, dados.nome, dados.descricao
        )
    except UniqueViolation:
        raise ConflitoError(f"Já existe outra categoria com o nome '{dados.nome}'.")

    if not atualizada:
        raise NaoEncontradoError(f"Categoria com id {categoria_id} não encontrada.")
    return atualizada


def deletar_categoria(categoria_id: int):
    try:
        deletou = categoria_repository.deletar(categoria_id)
    except ForeignKeyViolation:
        raise ConflitoError(
            "Não é possível excluir uma categoria que possui materiais vinculados."
        )

    if not deletou:
        raise NaoEncontradoError(f"Categoria com id {categoria_id} não encontrada.")


def deletar_categorias_em_lote(dados: CategoriaDeleteLote):
    ids_unicos = list(dict.fromkeys(dados.ids))

    try:
        ids_deletados = categoria_repository.deletar_em_lote(ids_unicos)
    except ForeignKeyViolation:
        raise ConflitoError(
            "Exclusão cancelada: uma ou mais categorias possuem materiais vinculados."
        )

    deletados_set = set(ids_deletados)
    ids_nao_encontrados = [cid for cid in ids_unicos if cid not in deletados_set]

    return {
        "ids_deletados": ids_deletados,
        "ids_nao_encontrados": ids_nao_encontrados,
        "total_deletado": len(ids_deletados),
    }



