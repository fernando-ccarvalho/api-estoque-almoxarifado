from psycopg.rows import dict_row

from app.database import conectar


def criar(
    con,
    material_id: int,
    tipo: str,
    quantidade: int,
    observacao: str | None,
):
    with con.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            INSERT INTO movimentacoes (
                material_id, tipo, quantidade, observacao
            )
            VALUES (%s, %s, %s, %s)
            RETURNING
                id, material_id, tipo, quantidade, observacao, data_movimentacao;
            """,
            (material_id, tipo, quantidade, observacao),
        )
        return cur.fetchone()


def listar(
    material_id: int | None = None,
    tipo: str | None = None,
):
    condicoes = []
    parametros = []

    if material_id is not None:
        condicoes.append("material_id = %s")
        parametros.append(material_id)

    if tipo is not None:
        condicoes.append("tipo = %s")
        parametros.append(tipo)

    where_sql = ""
    if condicoes:
        where_sql = "WHERE " + " AND ".join(condicoes)

    query = f"""
        SELECT
            id, material_id, tipo, quantidade, observacao, data_movimentacao
        FROM movimentacoes
        {where_sql}
        ORDER BY data_movimentacao DESC, id DESC;
    """

    with conectar() as con:
        with con.cursor(row_factory=dict_row) as cur:
            cur.execute(query, tuple(parametros))
            return cur.fetchall()


def buscar_por_id(movimentacao_id: int):
    with conectar() as con:
        with con.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT
                    id, material_id, tipo, quantidade, observacao, data_movimentacao
                FROM movimentacoes
                WHERE id = %s;
                """,
                (movimentacao_id,),
            )
            return cur.fetchone()     