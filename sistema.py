def insert_usuario(id_usuario):
    mycursor.execute(f"SELECT id_usuario FROM usuario WHERE id_usuario = {id_usuario};")
    if mycursor.fetchone() is None:
        mycursor.execute(f"INSERT INTO usuario (id_usuario) VALUES ({id_usuario});")

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