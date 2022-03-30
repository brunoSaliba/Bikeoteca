class Bike:
    def __init__(self, modelo, marca, modalidade, id=None):
        self.id = id
        self.modelo = modelo
        self.marca = marca
        self.modalidade = modalidade

    def __str__(self):
        return f'Modelo - {self.modelo}, Marca - {self.marca}, Modalidade - {self.modalidade}.'