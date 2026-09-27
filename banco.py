import sqlite3
import pandas as pd

NOME_BANCO = "biblioteca_v2.db"

def conectar():
    return sqlite3.connect(NOME_BANCO, check_same_thread=False)

def criar_tabela():
    conexao = conectar()
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS registro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            leitor TEXT NOT NULL,
            genero TEXT NOT NULL,
            livro TEXT NOT NULL,
            devolucao TEXT NOT NULL,
            data TEXT NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()

def inserir_registro(leitor, genero, livro, devolucao, data):
    conexao = conectar()
    conexao.execute(
        """
        INSERT INTO registro (leitor, genero, livro, devolucao, data)
        VALUES (?, ?, ?, ?, ?)
        """,
        (leitor, genero, livro, devolucao, data)
    )
    conexao.commit()
    conexao.close()

def listar_registro():
    conexao = conectar()
    df = pd.read_sql_query("SELECT * FROM registro ORDER BY id DESC", conexao)
    conexao.close()
    return df

def atualizar_devolucao(id_registro, novo_status="Sim"):
    conexao = conectar()
    conexao.execute(
        "UPDATE registro SET devolucao = ? WHERE id = ?",
        (novo_status, id_registro)
    )
    conexao.commit()
    conexao.close()

def excluir_registros(id_registro):
    conexao = conectar()
    conexao.execute("DELETE FROM registro WHERE id = ?", (id_registro,))
    conexao.commit()
    conexao.close()