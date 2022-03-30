import os
from bikeoteca import app

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo


def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    print(arquivo)
    os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))