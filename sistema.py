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
    

def insert_usuario(id_usuario):
    mycursor.execute(f"SELECT id_usuario FROM usuario WHERE id_usuario = {id_usuario};")
    if mycursor.fetchone() is None:
        mycursor.execute(f"INSERT INTO usuario (id_usuario) VALUES ({id_usuario});")