def get_or_create_plataforma(insert_plataforma):
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