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
            host = env_vars.host,
            user = env_vars.user,
            password = env_vars.password,
            database = env_vars.database,
        )
        mycursor = mydb.cursor()
        print("Conexão criada com sucesso. ✔️\n ")
    except Error:
        print(f"Não foi possível criar a conexão. {Error} ❌\n ")


def close_connection():
    if "mydb" in locals() and mydb.is_connected():
        mycursor.close()
        mydb.close()
    print("Conexão com o SGBD fechada.🔌🚫 \n")


def create_db():
    try:
        mycursor.execute("CREATE DATABASE IF NOT EXISTS globo_tech;")
        print("Banco de dados globo_tech criado com sucesso. ✔️\n")
    except Error:
        print(f"Não foi possível criar o banco de dados. {Error} ❌\n")

    try:
        mycursor.execute("USE globo_tech;")
        print("Banco de dados selecionado com sucesso. ✔️\n")
    except Error:
        print(f"Não foi possível selecionar o banco de dados. {Error} ❌\n")

    try:
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS usuario("
            "id_usuario BIGINT NOT NULL AUTO_INCREMENT, "
            "PRIMARY KEY (id_usuario));"
        )
        print("Tabela 'usuario' criada com sucesso. ✔️\n")
    except Error:
        print(f"Não foi possível criar a tabela 'usuario'. {Error} ❌\n")

    try:
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS conteudo("
            "id_conteudo SMALLINT NOT NULL AUTO_INCREMENT, "
            "nome_conteudo VARCHAR(100) NOT NULL, "
            "PRIMARY KEY (id_conteudo));"
        )
        print("Tabela 'conteudo' criada com sucesso. ✔️\n")
    except Error:
        print(f"Não foi possível criar a tabela 'conteudo'. {Error}\n ❌")

    try:
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS plataforma("
            "id_plataforma SMALLINT NOT NULL AUTO_INCREMENT, "
            "nome_plataforma VARCHAR(100) NOT NULL, "
            "PRIMARY KEY (id_plataforma));"
        )
        print("Tabela 'plataforma' criada com sucesso. ✔️\n")
    except Error:
        print(f"Não foi possível criar a tabela 'plataforma'. {Error} ❌\n")

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
        print("Tabela 'interacao' criada com sucesso. ✔️ \n")
    except Error:
        print(f"Não foi possível criar a tabela 'interacao'. {Error}\n ❌")


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


def insert_data_csv(path):
    try:
        df = pd.read_csv(path)
   
        try:
            for _, row in df.iterrows():
                insert_usuario(row["id_usuario"])
                insert_conteudo(row["id_conteudo"], row["nome_conteudo"])
                id_plataforma = insert_plataforma(row["plataforma"])
                inserir_interacao(row, id_plataforma)
            print("\nDados do CSV inseridos com sucesso. ✔️\n")
        except Error:
            print(f"Não foi possível carregar os dados do CSV. {Error} ❌\n")
    except:
        print(f'\nNome do arquivo invalido: {path} ❌ \n')
    



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


def conteudos_mais_comentados(top = 5):
    mycursor.execute(
        f"""
            SELECT
                i.id_conteudo, c.nome_conteudo, COUNT(*) AS total_comentarios
            FROM 
                interacao as i
            JOIN
                conteudo as c ON i.id_conteudo = c.id_conteudo
            WHERE 
                tipo_interacao = 'comment'
            GROUP BY 
                i.id_conteudo
            ORDER BY 
                total_comentarios DESC limit {top};

        """
    )
    return mycursor.fetchall()


def plataforma_maior_engajamento(top = 5):
    mycursor.execute(
        f"""            
            SELECT 
                p.id_plataforma,
                p.nome_plataforma,
                COUNT(*) AS total_interacoes
            FROM interacao AS i
            JOIN plataforma AS p ON p.id_plataforma = i.id_plataforma
            WHERE i.tipo_interacao != 'view_start'
            GROUP BY p.id_plataforma, p.nome_plataforma
            ORDER BY total_interacoes desc limit {top};
        """
    )
    return mycursor.fetchall()

def converter_segundos_para_horas(segundos):
    horas, resto = divmod(segundos, 3600)
    minutos, segundos = divmod(resto, 60)
    return f"{horas:02}:{minutos:02}:{segundos:02}"

def conteudo_maior_engajamento(top = 5):
    print(f"Iniciando")
    mycursor.execute(
        f"""            
            SELECT 
                c.id_conteudo,
                c.nome_conteudo,
                COUNT(*) AS total_interacoes_conteudo
            FROM conteudo AS c
            JOIN interacao AS i ON i.id_conteudo = c.id_conteudo
            WHERE i.tipo_interacao != 'view_start'
            GROUP BY c.id_conteudo, c.nome_conteudo
            ORDER BY total_interacoes_conteudo DESC LIMIT {top};
        """
    )
    print("Finalizando")
    return mycursor.fetchall()