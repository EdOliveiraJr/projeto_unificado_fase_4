import env_vars
import mysql.connector
from mysql.connector import Error
import pandas as pd

df = pd.read_csv('interacoes_globo.csv')

mydb = None
mycursor = None

def createConnection():
  try:
    global mydb
    global mycursor
    mydb = mysql.connector.connect(
      host = env_vars.host,
      user = env_vars.user,
      password = env_vars.password,
      database = env_vars.database,
    )
    mycursor = mydb.cursor()
    print("Conexão criada com sucesso.")
  except Error:
    print(f"Erro: {Error}") 

def closeConnection():
  if "mydb" in locals() and mydb.is_connected():
    mycursor.close()
    mydb.close()
  print("Conexão com o MySQL fechada.")

def create_db():
    try:
        mycursor.execute("CREATE DATABASE IF NOT EXISTS interacoes_globotech;")
        print("Banco de dados interacoes_globotech criado com sucesso.\n")
    except:
        print(f"Não foi possível criar o banco de dados. Erro: {e}\n")

    try:
        mycursor.execute("USE interacoes_globotech;")
        print("Banco de dados selecionado com sucesso.\n")
    except:
        print(f"Não foi possível selecionar o banco de dados. Erro: {e}\n")

    try:
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS usuario("
            "id_usuario BIGINT NOT NULL AUTO_INCREMENT, "
            "PRIMARY KEY (id_usuario));"
        )
        print("Tabela 'usuario' criada com sucesso.\n")
    except:
        print(f"Não foi possível criar a tabela 'usuario'. Erro: {e}\n")

    try:
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS conteudo("
            "id_conteudo SMALLINT NOT NULL AUTO_INCREMENT, "
            "nome_conteudo VARCHAR(100) NOT NULL, "
            "PRIMARY KEY (id_conteudo));"
        )
        print("Tabela 'conteudo' criada com sucesso.\n")
    except:
        print(f"Não foi possível criar a tabela 'conteudo'. Erro: {e}\n")

    try:
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS plataforma("
            "id_plataforma SMALLINT NOT NULL AUTO_INCREMENT, "
            "nome_plataforma VARCHAR(100) NOT NULL, "
            "PRIMARY KEY (id_plataforma));"
        )
        print("Tabela 'plataforma' criada com sucesso.\n")
    except:
        print(f"Não foi possível criar a tabela 'plataforma'. Erro: {e}\n")

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
    except:
        print(f"Não foi possível criar a tabela 'interacao'. Erro: {e}\n")

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