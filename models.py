from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    personas = db.relationship('Persona', backref='user')


class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(100))
    geslacht = db.Column(db.String(20))
    leeftijd = db.Column(db.Integer)
    school = db.Column(db.Text)
    werk = db.Column(db.Text)
    doelen = db.Column(db.Text)
    frustraties = db.Column(db.Text)
    

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Persona {self.naam}>"