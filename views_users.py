from flask import render_template, request, redirect, session, flash, url_for
from models import Usuarios
from helpers import *
from jogoteca2 import app
from flask_bcrypt import check_password_hash


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()

    if 'nome_usuario_logado' in session and session['nome_usuario_logado'] is not None:
        flash(session.get('nome_usuario_logado') + ' Já esta logado!')
        return redirect(proxima)

    print('proxima= ' + str(proxima))
    return render_template('/login.html', proxima=proxima, form=form)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    senha = check_password_hash(usuario.password, form.senha.data)
    if usuario and senha:

        session['nome_usuario_logado'] = usuario.nickname
        flash(usuario.nickname + ' logou com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    else:
        flash('Usuario não logado.')
        return redirect(url_for('login', proxima=url_for('cadastro')))


@app.route('/logout')
def logout():
    session['nome_usuario_logado'] = None
    flash('Logout realizado com sucesso')
    return redirect(url_for('index'))
