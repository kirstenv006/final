from flask import Flask, render_template, request, redirect, session
import os

from extensions import db
from models import User, Persona

# -----------------------------
# APP SETUP
# -----------------------------
app = Flask(__name__)
app.secret_key = "supersecretkey"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

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

    return render_template("stap1.html", step=1)


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

    return render_template("stap2.html", step=2)


# -----------------------------
# STAP 3 – Eigenschappen, doelen & frustraties
@app.route('/stap3', methods=['GET', 'POST'])
def stap3():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        if request.form.get('action') == 'prev':
            # optioneel: sla huidige session data op
            session['doelen'] = request.form.get('doelen', '')
            session['frustraties'] = request.form.get('frustraties', '')
            session['extravert'] = int(request.form.get('extravert', 3))
            session['creatief'] = int(request.form.get('creatief', 3))
            session['intuitief'] = int(request.form.get('intuitief', 3))
            session['stress'] = int(request.form.get('stress', 3))

            return redirect('/stap2')

        # normale 'Volgende'
        session['doelen'] = request.form.get('doelen', '')
        session['frustraties'] = request.form.get('frustraties', '')
        session['extravert'] = int(request.form.get('extravert', 3))
        session['creatief'] = int(request.form.get('creatief', 3))
        session['intuitief'] = int(request.form.get('intuitief', 3))
        session['stress'] = int(request.form.get('stress', 3))

        return redirect('/generate')

    return render_template("stap3.html", step=3)



# -----------------------------
# GENERATE – persona opslaan
@app.route('/generate')
def generate():
    if 'user_id' not in session:
        return redirect('/login')

    persona = Persona(
        naam=session.get('naam'),
        geslacht=session.get('geslacht'),
        leeftijd=int(session.get('leeftijd')) if session.get('leeftijd') else None,
        school=session.get('school'),
        werk=session.get('werk'),
        doelen=session.get('doelen'),
        frustraties=session.get('frustraties'),
        extravert=session.get('extravert'),
        creatief=session.get('creatief'),
        intuitief=session.get('intuitief'),
        stress=session.get('stress'),
        user_id=session['user_id']
    )

    db.session.add(persona)
    db.session.commit()

    # Session opschonen
    for key in [
        'naam', 'geslacht', 'leeftijd',
        'school', 'werk',
        'doelen', 'frustraties',
        'extravert', 'creatief', 'intuitief', 'stress'
    ]:
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

    return render_template('result.html', persona=persona, step=4)



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
