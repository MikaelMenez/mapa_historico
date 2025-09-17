import sqlite3

sql_connection=sqlite3.connect('app.db',check_same_thread=False)
sql_command_handler=sql_connection.cursor()
def create_table():
    
    sql_command_handler.execute('''
            CREATE TABLE IF NOT EXISTS pontos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            texto TEXT NOT NULL,
            imagem_path TEXT NOT NULL,
            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
            cord_x REAL NOT NULL,
            cord_y REAL NOT NULL
        )
    ''')

    sql_connection.commit()
def acessar_item(id:int)->list:
    sql_command_handler.execute(f"SELECT * FROM pontos WHERE id=?",(id))
    sql_connection.commit()

    return sql_command_handler.fetchall()
def adicionar_item(titulo:str,texto:str,imagem_path:str,data_criacao:str,cord_x:float,cord_y:float):
    sql_command_handler.execute(f"INSERT INTO pontos (titulo,texto,imagem_path,data_criacao,cord_x,cord_y) VALUES (?,?,?,?,?,?)",(titulo,texto,imagem_path,data_criacao,cord_x,cord_y))
    sql_connection.commit()

def deletar_item(id:int):
    sql_command_handler.execute(f'DELETE FROM pontos WHERE id=?',(id))
    sql_connection.commit()
def deletar_tudo():
    sql_command_handler.execute(f'DELETE FROM pontos')
    sql_connection.commit()

def atualizar_item(id:int,titulo:str,texto:str,imagem_path:str,data_criacao:str,cord_x:float,cord_y:float):
    sql_command_handler.execute(f'UPDATE pontos SET titulo=?,texto=?,imagem_path=?,data_criacao=?,cord_x=?,cord_y=? WHERE id=?',(titulo,texto,imagem_path,data_criacao,cord_x,cord_y,id))
    sql_connection.commit()

def acessar_todos()->list:
    sql_command_handler.execute("SELECT * FROM pontos")
    return sql_command_handler.fetchall()
def transformar_em_json(lista_tuplas):
    lista_json = []
    for item in lista_tuplas:
        d = {
            "id": item[0],
            "titulo": item[1],
            "texto": item[2],
            "imagem_path": item[3],
            "data_criacao": item[4],
            "cord_x": item[5],
            "cord_y": item[6]
        }
        lista_json.append(d)
    return lista_json
