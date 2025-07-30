-- Criação do Banco de Dados
CREATE DATABASE globo_tech;

USE globo_tech;

-- Script de criação da tabela usuario
CREATE TABLE usuario
    (
        id_usuario BIGINT NOT NULL AUTO_INCREMENT,
        nome_usuario VARCHAR(100) NOT NULL,
        PRIMARY KEY (id_usuario)
    );

-- Script de criação da tabela plataforma
CREATE TABLE plataforma
  (
    id_plataforma SMALLINT NOT NULL AUTO_INCREMENT,
    nome_plataforma VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_plataforma)
  );

-- Script de criação da tabela conteudo
CREATE TABLE conteudo
  (
    id_conteudo SMALLINT NOT NULL AUTO_INCREMENT,
    nome_conteudo VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_conteudo)
  );
  
-- Script de criação da tabela interacao
CREATE TABLE interacao
  (
    id_interacao BIGINT NOT NULL AUTO_INCREMENT,
    id_usuario BIGINT NOT NULL,
    id_conteudo SMALLINT NOT NULL,
    id_plataforma SMALLINT NOT NULL,
    comment_text TEXT,
    tipo_interacao VARCHAR(50) NOT NULL,
    watch_duration_seconds INT DEFAULT NULL,
    timestamp_interacao DATETIME NOT NULL,

    PRIMARY KEY(id_interacao),
    FOREIGN KEY(id_usuario) REFERENCES usuario(id_usuario)
    FOREIGN KEY(id_conteudo) REFERENCES conteudo(id_conteudo)
    FOREIGN KEY(id_plataforma) REFERENCES plataforma(id_plataforma)
  )

-- Script de inserção de dados usuario

-- Script de inserção de dados plataforma

-- Script de inserção de dados conteudo

-- Script de inserção de dados interacao

-- Script métrica conteudos_mais_consumidos

-- Script métrica plataforma_maior_engajamento

-- Script métrica conteudos_mais_comentados

-- Script métodos python de criação das tabelas
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



