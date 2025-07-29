-- Script de criação do banco de dados

-- Script de criação da tabela usuario

-- Script de criação da tabela plataforma

-- Script de criação da tabela conteudo

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
CREATE TABLE conteudo
  (
    id_conteudo SMALLINT NOT NULL AUTO_INCREMENT,
    nome_conteudo VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_conteudo)
  );


-- Script de inserção de dados interacao

-- Script métrica conteudos_mais_consumidos

-- Script métrica plataforma_maior_engajamento

-- Script métrica conteudos_mais_comentados