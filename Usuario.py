class Usuario:
    def __init__(self, id, usuario, senha):
        self.id = id
        self.usuario = usuario
        self.senha = senha

    def __str__(self):
        return f'Usuario - {self.usuario}'