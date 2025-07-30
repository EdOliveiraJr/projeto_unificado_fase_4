-- Criação do Banco de Dados
CREATE DATABASE IF NOT EXISTS globo_tech;

USE globo_tech;

-- Script de criação da tabela usuario
CREATE TABLE IF NOT EXISTS usuario 
  (
    id_usuario BIGINT NOT NULL AUTO_INCREMENT,
    nome_usuario VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_usuario)
  );

-- Script de criação da tabela plataforma
CREATE TABLE IF NOT EXISTS plataforma 
  (
    id_plataforma SMALLINT NOT NULL AUTO_INCREMENT,
    nome_plataforma VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_plataforma)
  );

-- Script de criação da tabela conteudo
CREATE TABLE IF NOT EXISTS conteudo
  (
    id_conteudo SMALLINT NOT NULL AUTO_INCREMENT,
    nome_conteudo VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_conteudo)
  );
  
-- Script de criação da tabela interacao
CREATE TABLE IF NOT EXISTS interacao
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
INSERT INTO usuario (id_usuario) VALUES (101);

-- Script de inserção de dados plataforma
INSERT INTO plataforma (nome_plataforma) VALUES ('TV Globo');

-- Script de inserção de dados conteudo
INSERT INTO conteudo (id_conteudo, nome_conteudo) VALUES (1, 'Jornal Nacional');

-- Script de inserção de dados interacao
INSERT INTO interacao (id_usuario, id_conteudo, id_plataforma, comment_text, tipo_interacao, watch_duration_seconds, timestamp_interacao)
VALUES
(101, 1, 1, NULL, 'view_start', 1800, '2024-10-20 20:05:12');

-- Script métrica conteudos_mais_consumidos
SELECT
    i.id_conteudo,
    c.nome_conteudo,
    SUM(COALESCE(CAST(i.watch_duration_seconds AS UNSIGNED), 0)) AS tempo_total_consumo_segundos
FROM
    interacao as i
JOIN
    conteudo as c ON i.id_conteudo = c.id_conteudo
GROUP BY
    i.id_conteudo, c.nome_conteudo
ORDER BY
    tempo_total_consumo_segundos DESC
LIMIT 5;

-- Script métrica plataforma_maior_engajamento
SELECT 
    p.id_plataforma,
    p.nome_plataforma,
    COUNT(*) AS total_interacoes
FROM interacao AS i
JOIN plataforma AS p ON p.id_plataforma = i.id_plataforma
WHERE i.tipo_interacao != 'view_start'
GROUP BY p.id_plataforma, p.nome_plataforma
ORDER BY total_interacoes DESC
LIMIT 5;

-- Script métrica conteudos_mais_comentados
SELECT
    i.id_conteudo,
    c.nome_conteudo,
    COUNT(*) AS total_comentarios
FROM 
    interacao as i
JOIN
    conteudo as c ON i.id_conteudo = c.id_conteudo
WHERE 
    tipo_interacao = 'comment'
GROUP BY 
    i.id_conteudo
ORDER BY 
    total_comentarios DESC
LIMIT 5;





