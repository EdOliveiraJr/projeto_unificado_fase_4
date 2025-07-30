import env_vars
import mysql.connector
from mysql.connector import Error
import pandas as pd

mydb = None
mycursor = None


def create_connection():
    try:
        global mydb
        global mycursor
        mydb = mysql.connector.connect(
            host=env_vars.host,
            user=env_vars.user,
            password=env_vars.password,
            database=env_vars.database,
        )
        mycursor = mydb.cursor()
        print("Conexão criada com sucesso.")
    except Error:
        print(f"Erro: {Error}")


def close_connection():
    if "mydb" in locals() and mydb.is_connected():
        mycursor.close()
        mydb.close()
    print("Conexão com o MySQL fechada.")


def create_db():
    try:
        mycursor.execute("CREATE DATABASE IF NOT EXISTS globo_tech;")
        print("Banco de dados globo_tech criado com sucesso.\n")
    except Error:
        print(f"Não foi possível criar o banco de dados. Erro: {Error}\n")

    try:
        mycursor.execute("USE globo_tech;")
        print("Banco de dados selecionado com sucesso.\n")
    except Error:
        print(f"Não foi possível selecionar o banco de dados. Erro: {Error}\n")

    try:
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS usuario("
            "id_usuario BIGINT NOT NULL AUTO_INCREMENT, "
            "PRIMARY KEY (id_usuario));"
        )
        print("Tabela 'usuario' criada com sucesso.\n")
    except Error:
        print(f"Não foi possível criar a tabela 'usuario'. Erro: {Error}\n")

    try:
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS conteudo("
            "id_conteudo SMALLINT NOT NULL AUTO_INCREMENT, "
            "nome_conteudo VARCHAR(100) NOT NULL, "
            "PRIMARY KEY (id_conteudo));"
        )
        print("Tabela 'conteudo' criada com sucesso.\n")
    except Error:
        print(f"Não foi possível criar a tabela 'conteudo'. Erro: {Error}\n")

    try:
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS plataforma("
            "id_plataforma SMALLINT NOT NULL AUTO_INCREMENT, "
            "nome_plataforma VARCHAR(100) NOT NULL, "
            "PRIMARY KEY (id_plataforma));"
        )
        print("Tabela 'plataforma' criada com sucesso.\n")
    except Error:
        print(f"Não foi possível criar a tabela 'plataforma'. Erro: {Error}\n")

    try:
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS interacao("
            "id_interacao BIGINT NOT NULL AUTO_INCREMENT, "
            "id_usuario BIGINT NOT NULL, "
            "id_conteudo SMALLINT NOT NULL, "
            "id_plataforma SMALLINT NOT NULL, "
            "comment_text TEXT, "
            "tipo_interacao VARCHAR(50) NOT NULL, "
            "watch_duration_seconds INT DEFAULT NULL, "
            "timestamp_interacao DATETIME NOT NULL, "
            "PRIMARY KEY (id_interacao), "
            "FOREIGN KEY (id_conteudo) REFERENCES conteudo(id_conteudo), "
            "FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario), "
            "FOREIGN KEY (id_plataforma) REFERENCES plataforma(id_plataforma));"
        )
        print("Tabela 'interacao' criada com sucesso.\n")
    except Error:
        print(f"Não foi possível criar a tabela 'interacao'. Erro: {Error}\n")


def insert_usuario(id_usuario):
    mycursor.execute(f"SELECT id_usuario FROM usuario WHERE id_usuario = {id_usuario};")
    if mycursor.fetchone() is None:
        mycursor.execute(f"INSERT INTO usuario (id_usuario) VALUES ({id_usuario});")


def insert_plataforma(nome_plataforma):
    mycursor.execute(
        f'SELECT id_plataforma FROM plataforma WHERE nome_plataforma = "{nome_plataforma}";'
    )
    resultado = mycursor.fetchone()
    if resultado:
        return resultado[0]
    else:
        mycursor.execute(
            f'INSERT INTO plataforma (nome_plataforma) VALUES ("{nome_plataforma}");'
        )
        mydb.commit()
        return mycursor.lastrowid


def insert_conteudo(id_conteudo, nome_conteudo):
    mycursor.execute(
        f"SELECT id_conteudo FROM conteudo WHERE id_conteudo = {id_conteudo};"
    )
    if mycursor.fetchone() is None:
        mycursor.execute(
            f'INSERT INTO conteudo (id_conteudo, nome_conteudo) VALUES ({id_conteudo}, "{nome_conteudo}");'
        )


def inserir_interacao(row, id_plataforma):
    mycursor.execute(
        f"""
        INSERT INTO interacao (
            id_usuario, id_conteudo, id_plataforma,
            comment_text, tipo_interacao,
            watch_duration_seconds, timestamp_interacao
        ) VALUES ({row["id_usuario"]},
                  {row["id_conteudo"]}, 
                  {id_plataforma},
                  "{row["comment_text"] if pd.notna(row["comment_text"]) else ""}",
                  "{row["tipo_interacao"]}",
                  {int(row["watch_duration_seconds"]) if pd.notna(row["watch_duration_seconds"]) else 0},
                  "{row["timestamp_interacao"]}")
    """
    )


def insert_data_csv(path_csv):
    try:
        print(f"Iniciando o carregamento dos dados do CSV {path_csv}...")
        df = pd.read_csv(path_csv)
        try:
            for _, row in df.iterrows():
                insert_usuario(row["id_usuario"])
                insert_conteudo(row["id_conteudo"], row["nome_conteudo"])
                id_plataforma = insert_plataforma(row["plataforma"])
                inserir_interacao(row, id_plataforma)
            print("Dados do CSV inseridos com sucesso.")
        except Error:
            print(f"Não foi possível carregar os dados do CSV - {Error}")

    except:
        print("Não foi possível encontrar o CSV")


def conteudos_mais_consumidos(top = 5):
    mycursor.execute(
        f'''
            SELECT
                i.id_conteudo,
                c.nome_conteudo,
                -- A função SUM() soma os valores.
                -- A função COALESCE() trata os valores nulos/vazios como 0 para não dar erro na soma.
                -- A função CAST() converte o texto para um número inteiro (INT).
                SUM(COALESCE(CAST(i.watch_duration_seconds AS UNSIGNED), 0)) AS tempo_total_consumo_segundos
            FROM
                interacao as i
            JOIN
                conteudo as c ON i.id_conteudo = c.id_conteudo
            GROUP BY
                i.id_conteudo, c.nome_conteudo
            ORDER BY
                tempo_total_consumo_segundos DESC LIMIT {top};
        '''
    )
    return mycursor.fetchall()
