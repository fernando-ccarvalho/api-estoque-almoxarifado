from psycopg.rows import dict_row
from app.database import conectar

# cria categorias para a tabela
def criar(nome: str, descricao: str | None):
    with conectar() as con:
        with con.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO categorias (nome, descricao)
                VALUES (%s, %s)
                RETURNING id, nome, descricao
                """,
                (nome, descricao),
            )
            return cur.fetchone()

# lista todas as categorias
def listar_todas():
    with conectar() as con:
        with con.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT id, nome, descricao FROM categorias ORDER BY id"
            )
            return cur.fetchall()

def buscar_por_id(categoria_id: int):
    with conectar() as con:
        with con.cursor(row_factory=dict_row) as cur:
                cur.execute(
                     "SELECT id, nome, descricao from categorias WHERE id = %s",
                     (categoria_id,),
                )
                return cur.fetchone()

def buscar_por_nome(nome:str):
    with conectar() as con:
        with con.cursor(row_factory=dict_row) as cur:
                cur.execute(
                     "SELECT id, nome, descricao FROM categorias WHERE LOWER (nome)= LOWER(%s)",
                    (nome,),
                )
                return cur.fetchone()

def atualizar(categoria_id: int, nome: str, descricao:str | None):
    with conectar() as con:
        with con.cursor(row_factory=dict_row) as cur:
                cur.execute(
                     """
                     UPDATE categorias 
                     SET nome = %s, descricao = %s
                     WHERE id = %s
                     RETURNING id, nome, descricao
                     """,
                     (nome, descricao, categoria_id),
                )
                return cur.fetchone()

def deletar(categoria_id: int):
    with conectar() as con:
        with con.cursor() as cur:
                cur.execute(
                     "DELETE FROM categorias WHERE id = %s",
                     (categoria_id,),
                )
                return cur.rowcount > 0 

def criar_em_lote(categorias: list[dict]):
    if not categorias:
        return []

    valores = [(item["nome"], item["descricao"]) for item in categorias]

    with conectar() as con:
        with con.cursor(row_factory=dict_row) as cur:
            cur.executemany(
                """
                INSERT INTO categorias (nome, descricao)
                VALUES (%s, %s)
                RETURNING id, nome, descricao
                """,
                valores,
                returning=True,
            )

            criadas = []
            while True:
                linha = cur.fetchone()
                if linha:
                    criadas.append(linha)
                if not cur.nextset():
                    break

            return criadas


def buscar_por_nomes(nomes: list[str]):
    if not nomes:
        return []

    nomes_lower = [nome.lower() for nome in nomes]

    with conectar() as con:
        with con.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT id, nome, descricao FROM categorias WHERE LOWER(nome) = ANY(%s)",
                (nomes_lower,),
            )
            return cur.fetchall()


def deletar_em_lote(categoria_ids: list[int]) -> list[int]:
    if not categoria_ids:
        return []

    with conectar() as con:
        with con.cursor() as cur:
            cur.execute(
                "DELETE FROM categorias WHERE id = ANY(%s) RETURNING id",
                (categoria_ids,),
            )
            return [linha[0] for linha in cur.fetchall()]