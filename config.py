import os

SECRET_KEY= 'albert'

SQLALCHEMY_DATABASE_URI = \
'{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGBD = 'mysql+mysqlconnector',
    usuario = 'root',
    senha = '30794009',
    servidor = 'localhost',
    database = 'jogoteca'
)

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__))+'/uploads'
