from psycopg.errors import CheckViolation, ForeignKeyViolation

from app.database import conectar
from app.exceptions import ConflitoError, NaoEncontradoError
from app.repositories import material_repository, movimentacao_repository
from app.schemas.movimentacao_schema import MovimentacaoCreate, TipoMovimentacao


def registrar_movimentacao(dados: MovimentacaoCreate):
    try:
        with conectar() as con:
            material = material_repository.buscar_por_id_com_trava(
                con, dados.material_id
            )
            if not material:
                raise NaoEncontradoError(
                    f"Material com ID {dados.material_id} não encontrado."
                )

            if not material["ativo"]:
                raise ConflitoError(
                    f"Material com ID {dados.material_id} está inativo e não pode ser movimentado."
                )

            if dados.tipo == "SAIDA" and material["saldo_atual"] < dados.quantidade:
                raise ConflitoError(
                    f"Saldo insuficiente para o material ID {dados.material_id}. "
                    f"Saldo atual: {material['saldo_atual']}, solicitado: {dados.quantidade}."
                )

            variacao = (
                dados.quantidade if dados.tipo == "ENTRADA" else -dados.quantidade
            )
            material_repository.atualizar_saldo(
                con, dados.material_id, variacao
            )

            return movimentacao_repository.criar(
                con,
                dados.material_id,
                dados.tipo,
                dados.quantidade,
                dados.observacao,
            )
    except CheckViolation:
        raise ConflitoError(
            "Operação bloqueada pelas regras de integridade do estoque."
        )
    except ForeignKeyViolation:
        raise NaoEncontradoError(
            f"Material com ID {dados.material_id} não encontrado."
        )


def listar_movimentacoes(
    material_id: int | None = None,
    tipo: TipoMovimentacao | None = None,
):
    return movimentacao_repository.listar(
        material_id=material_id,
        tipo=tipo,
    )


def buscar_movimentacao_por_id(movimentacao_id: int):
    movimentacao = movimentacao_repository.buscar_por_id(movimentacao_id)
    if not movimentacao:
        raise NaoEncontradoError(
            f"Movimentação com ID {movimentacao_id} não encontrada."
        )
    return movimentacao