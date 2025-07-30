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