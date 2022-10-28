from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca2 import app
from models import Jogos,db
import time
from helpers import *

from flask_bcrypt import check_password_hash


@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', jogos=lista)


@app.route('/cadastro-jogo')
def cadastro():
    if 'nome_usuario_logado' not in session or session['nome_usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('cadastro')))
    form = FormularioJogoCadastro()
    return render_template('/cadastro-jogo.html', titulo='Novo Jogo', form=form)



@app.route('/criar', methods=['POST', ])
def criar():
    form = FormularioJogoCadastro(request.form)

    if not form.validate_on_submit():
        flash('Formulario Invalido')
        return redirect(url_for('cadastro'))

    name = form.name.data
    game_type = form.game_type.data
    console = form.console.data

    jogo = Jogos.query.filter_by(name=name).first()

    if jogo:
        flash('Jogo já existente')
        return redirect(url_for('index'))

    else:
        jogo = Jogos(name=name, game_type=game_type, console=console)
        db.session.add(jogo)
        db.session.commit()
        flash(jogo.name + ' adicionado com sucesso.')

    arquivo = request.files['img_file']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa-{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))




@app.route('/editar/<int:id>')
def editar(id):
    if 'nome_usuario_logado' not in session or session['nome_usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))

    jogo = Jogos.query.filter_by(id=id).first()
    game_cover = recupera_imagem(id)
    form = FormularioJogoAtualizacao(request.form)
    form.console.data = jogo.console
    form.game_type.data = jogo.game_type

    return render_template('/editar.html', titulo='Editando Jogo', jogo=jogo, game_cover=game_cover, form=form)


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    form = FormularioJogoAtualizacao(request.form)

    if form.validate_on_submit():
        print('game id = ' + request.form['id'])
        jogo = Jogos.query.filter_by(id=request.form['id']).first()

        jogo.console = form.console.data
        jogo.game_type = form.game_type.data

        db.session.commit()

        arquivo = request.files['img_file']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()

        if arquivo.filename !='':
            delete_img(jogo.id)
            arquivo.save(f'{upload_path}/capa-{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    if 'nome_usuario_logado' not in session or session['nome_usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('index')))

    jogo = Jogos.query.filter_by(id=id).first()
    nome_do_jogo = jogo.name
    delete_img(jogo.id)
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()

    flash(nome_do_jogo + ' deletado com sucesso')

    return redirect(url_for('index'))


@app.route('/uploads/<img_file_name>')
def imagem(img_file_name):
    print('img_file_name = ' + img_file_name)
    return send_from_directory('uploads', img_file_name)
