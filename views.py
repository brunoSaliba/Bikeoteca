from Bike import Bike
from dao import BikeDao, UsuarioDao
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
import time
from bikeoteca import db, app
from utils import *

bike_dao = BikeDao(db)
usuario_dao = UsuarioDao(db)


@app.route('/')
def index():
    lista = bike_dao.listar()
    return render_template('lista.html', titulo='Bikes', bikes=lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Nova Bike')


@app.route('/criar', methods=['POST', ])
def criar():
    marca = request.form['marca']
    modelo = request.form['modelo']
    modalidade = request.form['modalidade']
    bike = Bike(marca, modelo, modalidade)
    bike = bike_dao.salvar(bike)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{bike.id}-{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    bike = bike_dao.busca_por_id(id)
    nome_imagem = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Jogo', bike=bike
                           , capa_bike=nome_imagem or 'capa_padrao.jpg')


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    marca = request.form['marca']
    modelo = request.form['modelo']
    modalidade = request.form['modalidade']
    bike = Bike(marca, modelo, modalidade, id=request.form['id'])

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(bike.id)
    arquivo.save(f'{upload_path}/capa{bike.id}-{timestamp}.jpg')
    bike_dao.salvar(bike)
    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    bike_dao.deletar(id)
    flash('A bike foi excluída com sucesso!')
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    print(usuario.usuario, usuario.senha, usuario.id)
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.usuario + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Não logado, tente denovo!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)
