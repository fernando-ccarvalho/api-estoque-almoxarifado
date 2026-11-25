from psycopg.errors import ForeignKeyViolation, UniqueViolation

from app.exceptions import ConflitoError, NaoEncontradoError
from app.repositories import categoria_repository, material_repository
from app.schemas.material_schema import MaterialCreate, MaterialUpdate


def criar_material(dados: MaterialCreate):
    categoria = categoria_repository.buscar_por_id(dados.categoria_id)
    if not categoria:
        raise NaoEncontradoError(
            f"Categoria com ID {dados.categoria_id} não encontrada."
        )

    if material_repository.buscar_por_sku(dados.sku):
        raise ConflitoError(
            f"Já existe um material cadastrado com o SKU '{dados.sku}'."
        )

    try:
        return material_repository.criar(
            dados.sku,
            dados.nome,
            dados.categoria_id,
            dados.unidade_medida,
            dados.estoque_minimo,
        )
    except UniqueViolation:
        raise ConflitoError(
            f"Já existe um material cadastrado com o SKU '{dados.sku}'."
        )
    except ForeignKeyViolation:
        raise NaoEncontradoError(
            f"Categoria com ID {dados.categoria_id} não encontrada."
        )


def listar_materiais(apenas_ativos: bool = True):
    return material_repository.listar_todos(apenas_ativos=apenas_ativos)


def buscar_material_por_id(material_id: int):
    material = material_repository.buscar_por_id(material_id)
    if not material:
        raise NaoEncontradoError(f"Material com ID {material_id} não encontrado.")
    return material


def atualizar_material(material_id: int, dados: MaterialUpdate):
    material = material_repository.buscar_por_id(material_id)
    if not material:
        raise NaoEncontradoError(f"Material com ID {material_id} não encontrado.")

    categoria = categoria_repository.buscar_por_id(dados.categoria_id)
    if not categoria:
        raise NaoEncontradoError(
            f"Categoria com ID {dados.categoria_id} não encontrada."
        )

    existente = material_repository.buscar_por_sku(dados.sku)
    if existente and existente["id"] != material_id:
        raise ConflitoError(
            f"Já existe outro material cadastrado com o SKU '{dados.sku}'."
        )

    try:
        atualizado = material_repository.atualizar(
            material_id,
            dados.sku,
            dados.nome,
            dados.categoria_id,
            dados.unidade_medida,
            dados.estoque_minimo,
        )
    except UniqueViolation:
        raise ConflitoError(
            f"Já existe outro material cadastrado com o SKU '{dados.sku}'."
        )
    except ForeignKeyViolation:
        raise NaoEncontradoError(
            f"Categoria com ID {dados.categoria_id} não encontrada."
        )

    if not atualizado:
        raise NaoEncontradoError(f"Material com ID {material_id} não encontrado.")

    return atualizado


def inativar_material(material_id: int):
    material = material_repository.buscar_por_id(material_id)
    if not material:
        raise NaoEncontradoError(f"Material com ID {material_id} não encontrado.")

    if not material["ativo"]:
        raise ConflitoError(f"Material com ID {material_id} já está inativo.")

    inativado = material_repository.inativar(material_id)
    if not inativado:
        raise NaoEncontradoError(f"Material com ID {material_id} não encontrado.")

    return inativado