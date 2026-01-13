from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import os

# -----------------------------
# APP SETUP
# -----------------------------
app = Flask(__name__)
app.secret_key = "supersecretkey"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------------
# MODELS
# -----------------------------
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

    school = db.Column(db.String(100))
    werk = db.Column(db.String(100))

    doelen = db.Column(db.Text)
    frustraties = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# -----------------------------
# DATABASE AANMAKEN
# -----------------------------
with app.app_context():
    db.create_all()

# -----------------------------
# ROUTES
# -----------------------------

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/stap1')
    return redirect('/login')


# -----------------------------
# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form['username'],
            password=request.form['password']
        ).first()

        if user:
            session['user_id'] = user.id
            return redirect('/stap1')

        return "Login mislukt"

    return render_template('login.html')


# -----------------------------
# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(username=request.form['username']).first():
            return "Gebruikersnaam bestaat al"

        user = User(
            username=request.form['username'],
            password=request.form['password']
        )
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        return redirect('/stap1')

    return render_template('register.html')


# -----------------------------
# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# -----------------------------
# STAP 1 – Persoonlijke info
@app.route('/stap1', methods=['GET', 'POST'])
def stap1():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        session['naam'] = request.form.get('naam', '')
        session['geslacht'] = request.form.get('geslacht', '')
        session['leeftijd'] = request.form.get('leeftijd', '')
        return redirect('/stap2')

    return render_template('stap1.html')


# -----------------------------
# STAP 2 – School & werk
@app.route('/stap2', methods=['GET', 'POST'])
def stap2():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        session['school'] = request.form.get('school', '')
        session['werk'] = request.form.get('werk', '')
        return redirect('/stap3')

    return render_template('stap2.html')


# -----------------------------
# STAP 3 – Doelen & frustraties
@app.route('/stap3', methods=['GET', 'POST'])
def stap3():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        session['doelen'] = request.form.get('doelen', '')
        session['frustraties'] = request.form.get('frustraties', '')
        return redirect('/generate')

    return render_template('stap3.html')


# -----------------------------
# GENERATE – persona opslaan
@app.route('/generate')
def generate():
    if 'user_id' not in session:
        return redirect('/login')

    new_persona = Persona(
        naam=session.get('naam'),
        geslacht=session.get('geslacht'),
        leeftijd=int(session.get('leeftijd')) if session.get('leeftijd') else None,
        school=session.get('school'),
        werk=session.get('werk'),
        doelen=session.get('doelen'),
        frustraties=session.get('frustraties'),
        user_id=session['user_id']
    )

    db.session.add(new_persona)
    db.session.commit()

    # Session opschonen
    for key in ['naam', 'geslacht', 'leeftijd', 'school', 'werk', 'doelen', 'frustraties']:
        session.pop(key, None)

    return redirect('/result')


# -----------------------------
# RESULT
@app.route('/result')
def result():
    if 'user_id' not in session:
        return redirect('/login')

    persona = Persona.query.filter_by(
        user_id=session['user_id']
    ).order_by(Persona.id.desc()).first()

    if not persona:
        return redirect('/stap1')

    return render_template('result.html', persona=persona)


# -----------------------------
# MIJN PERSONA’S
@app.route('/personas')
def personas():
    if 'user_id' not in session:
        return redirect('/login')

    personas = Persona.query.filter_by(user_id=session['user_id']).all()
    return render_template('personas.html', personas=personas)


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
