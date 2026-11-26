from psycopg.rows import dict_row

from app.database import conectar


def criar(
    sku: str,
    nome: str,
    categoria_id: int,
    unidade_medida: str,
    estoque_minimo: int,
):
    with conectar() as con:
        with con.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO materiais (
                    sku, nome, categoria_id, unidade_medida, estoque_minimo
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING
                    id, sku, nome, categoria_id, unidade_medida,
                    saldo_atual, estoque_minimo, ativo, criado_em;
                """,
                (sku, nome, categoria_id, unidade_medida, estoque_minimo),
            )
            return cur.fetchone()


def listar_todos(apenas_ativos: bool = True):
    with conectar() as con:
        with con.cursor(row_factory=dict_row) as cur:
            if apenas_ativos:
                cur.execute(
                    """
                    SELECT
                    id, sku, nome, categoria_id, unidade_medida,
                    saldo_atual, estoque_minimo, ativo, criado_em
                    FROM materiais
                    WHERE ativo = TRUE
                    ORDER BY id;
                    """
                )
            else:
                cur.execute(
                    """
                    SELECT
                    id, sku, nome, categoria_id, unidade_medida,
                    saldo_atual, estoque_minimo, ativo, criado_em
                    FROM materiais
                    ORDER BY id;
                    """
                )
            return cur.fetchall()


def buscar_por_id(material_id: int):
    with conectar() as con:
        with con.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT
                id, sku, nome, categoria_id, unidade_medida,
                saldo_atual, estoque_minimo, ativo, criado_em
                FROM materiais
                WHERE id = %s;
                """,
                (material_id,),
            )
            return cur.fetchone()


def buscar_por_sku(sku: str):
    with conectar() as con:
        with con.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT
                id, sku, nome, categoria_id, unidade_medida,
                saldo_atual, estoque_minimo, ativo, criado_em
                FROM materiais
                WHERE LOWER(sku) = LOWER(%s);
                """,
                (sku,),
            )
            return cur.fetchone()


def atualizar(
    material_id: int,
    sku: str,
    nome: str,
    categoria_id: int,
    unidade_medida: str,
    estoque_minimo: int,
):
    with conectar() as con:
        with con.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                UPDATE materiais
                SET sku = %s,
                nome = %s,
                categoria_id = %s,
                unidade_medida = %s,
                estoque_minimo = %s
                WHERE id = %s
                RETURNING
                    id, sku, nome, categoria_id, unidade_medida,
                    saldo_atual, estoque_minimo, ativo, criado_em;
                """,
                (sku, nome, categoria_id, unidade_medida, estoque_minimo, material_id),
            )
            return cur.fetchone()


def inativar(material_id: int):
    with conectar() as con:
        with con.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                UPDATE materiais
                SET ativo = FALSE
                WHERE id = %s
                RETURNING
                    id, sku, nome, categoria_id, unidade_medida,
                    saldo_atual, estoque_minimo, ativo, criado_em;
                """,
                (material_id,),
            )
            return cur.fetchone()


def buscar_por_id_com_trava(con, material_id: int):
    with con.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            SELECT
                id, sku, nome, categoria_id, unidade_medida,
                saldo_atual, estoque_minimo, ativo, criado_em
            FROM materiais
            WHERE id = %s
            FOR UPDATE;
            """,
            (material_id,),
        )
        return cur.fetchone()


def atualizar_saldo(con, material_id: int, variacao: int):
    with con.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            UPDATE materiais
            SET saldo_atual = saldo_atual + %s
            WHERE id = %s
            RETURNING id, saldo_atual;
            """,
            (variacao, material_id),
        )
        return cur.fetchone()