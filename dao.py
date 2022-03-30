from Bike import Bike
from Usuario import Usuario

SQL_DELETA_BIKE = 'delete from bike where id = %s'
SQL_BIKE_POR_ID = 'SELECT id, modelo, marca, modalidade from bike where id = %s'
SQL_USUARIO_POR_ID = 'SELECT id, usuario, senha from usuario where usuario = %s'
SQL_ATUALIZA_BIKE = 'UPDATE bike SET modelo=%s, marca=%s, modalidade=%s where id = %s'
SQL_BUSCA_BIKES = 'SELECT id, modelo, marca, modalidade from bike'
SQL_CRIA_BIKE = 'INSERT into bike (modelo, marca, modalidade) values (%s, %s, %s)'

class BikeDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, bike):
        cursor = self.__db.connection.cursor()

        if (bike.id):
            cursor.execute(SQL_ATUALIZA_BIKE, (bike.modelo, bike.marca, bike.modalidade, bike.id))
        else:
            cursor.execute(SQL_CRIA_BIKE, (bike.modelo, bike.marca, bike.modalidade))
            bike.id = cursor.lastrowid
        self.__db.connection.commit()
        return bike

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_BIKES)
        bikes = traduz_bikes(cursor.fetchall())
        return bikes

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BIKE_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Bike(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_BIKE, (id, ))
        self.__db.connection.commit()


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario

def traduz_bikes(bikes):
    def cria_bike_com_tupla(tupla):
        return Bike(modelo=tupla[1], marca=tupla[2], modalidade=tupla[3], id=tupla[0])
    return list(map(cria_bike_com_tupla, bikes))

def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])
