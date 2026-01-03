from app import db 

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(50), nullable=False)
    leeftijd = db.Column(db.Integer, nullable=False)
    doelen = db.Column(db.String(200), nullable=False)
    frustraties = db.Column(db.String(200), nullable=False)
    interesses = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Persona {self.naam}>"
