def insert_usuario(id_usuario):
    mycursor.execute(f"SELECT id_usuario FROM usuario WHERE id_usuario = {id_usuario};")
    if mycursor.fetchone() is None:
        mycursor.execute(f"INSERT INTO usuario (id_usuario) VALUES ({id_usuario});")

def insert_conteudo(id_conteudo, nome_conteudo):
    mycursor.execute(
        f"SELECT id_conteudo FROM conteudo WHERE id_conteudo = {id_conteudo};"
    )
    if mycursor.fetchone() is None:
        mycursor.execute(
            f'INSERT INTO conteudo (id_conteudo, nome_conteudo) VALUES ({id_conteudo}, "{nome_conteudo}");'
        )