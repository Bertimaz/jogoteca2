import os
from jogoteca2 import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField


class FormularioJogoCadastro(FlaskForm):
    name = StringField('Nome do Jogo',
                       [validators.DataRequired(message="Forneça o nome do jogo"), validators.Length(min=1, max=50)])
    game_type = StringField('Categoria', [validators.DataRequired(message="Forneça a categoria do jogo"),
                                          validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(message="Forneça o console do jogo"),
                                      validators.Length(min=1, max=20)])
    save = SubmitField('Salvar')


class FormularioJogoAtualizacao(FlaskForm):
    game_type = StringField('Categoria', [validators.DataRequired(message="Forneça a categoria do jogo"),
                                          validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(message="Forneça o console do jogo"),
                                      validators.Length(min=1, max=20)])
    save = SubmitField('Salvar')


class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname',
                           [validators.DataRequired(message="Forneça o Nickname"), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha',
                               [validators.DataRequired(message="Forneça a Senha"), validators.Length(min=1, max=100)])
    login = SubmitField('Login')


def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa-{id}' in nome_arquivo:
            return nome_arquivo

    return 'capa_padrao.jpg'


def delete_img(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))
