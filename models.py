from jogoteca2 import db

class Jogos (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    game_type = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name
