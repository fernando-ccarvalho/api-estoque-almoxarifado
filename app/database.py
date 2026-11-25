import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def conectar():
    return psycopg.connect(

        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
        )

if __name__ == "__main__":
    try:
        with conectar() as con:
            with con.cursor() as cur:
                cur.execute("SELECT version();")
                print("Conectado ao PostgreSQL com sucesso!")
                print(cur.fetchone()[0])

    except Exception as erro:
        print(f"Erro ao conectar: {erro}")