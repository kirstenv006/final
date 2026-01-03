from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# -----------------------------
# DATABASE CONFIG
# -----------------------------
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# -----------------------------
# INIT DB
# -----------------------------
db = SQLAlchemy(app)

# -----------------------------
# MODELS IMPORT
# -----------------------------
from models import Persona

# -----------------------------
# CREATE DATABASE (1x)
# -----------------------------
with app.app_context():
    db.create_all()

# -----------------------------
# ROUTES
# -----------------------------

# Startpagina
@app.route('/')
def index():
    return render_template('index.html')

# -----------------------------
# STAP 1 – Persoonlijke info
@app.route('/stap1', methods=['GET', 'POST'])
def stap1():
    if request.method == 'POST':
        session['naam'] = request.form.get('naam')
        session['leeftijd'] = request.form.get('leeftijd')
        return redirect('/stap2')
    return render_template('stap1.html')

# -----------------------------
# STAP 2 – Doelen & frustraties
@app.route('/stap2', methods=['GET', 'POST'])
def stap2():
    if request.method == 'POST':
        session['doelen'] = request.form.get('doelen')
        session['frustraties'] = request.form.get('frustraties')
        return redirect('/stap3')
    return render_template('stap2.html')

# -----------------------------
# STAP 3 – Interesses
@app.route('/stap3', methods=['GET', 'POST'])
def stap3():
    if request.method == 'POST':
        session['interesses'] = request.form.get('interesses')
        return redirect('/generate')
    return render_template('stap3.html')

# -----------------------------
# GENERATE – opslaan in database
@app.route('/generate')
def generate():
    # 1️⃣ Haal alle data uit session
    persona_data = {
        'naam': session.get('naam'),
        'leeftijd': session.get('leeftijd'),
        'doelen': session.get('doelen'),
        'frustraties': session.get('frustraties'),
        'interesses': session.get('interesses')
    }

    # 2️⃣ Maak een nieuwe Persona
    new_persona = Persona(
        naam=persona_data['naam'],
        leeftijd=int(persona_data['leeftijd']),
        doelen=persona_data['doelen'],
        frustraties=persona_data['frustraties'],
        interesses=persona_data['interesses']
    )

    # 3️⃣ Voeg toe aan database
    db.session.add(new_persona)

    # 4️⃣ Sla op (commit)
    db.session.commit()

    # 5️⃣ Zet session data voor result pagina
    session['persona'] = persona_data

    # 6️⃣ Leeg de form data (zodat volgende run leeg is)
    for key in ['naam', 'leeftijd', 'doelen', 'frustraties', 'interesses']:
        session.pop(key, None)

    # 7️⃣ Redirect naar resultaatpagina
    return redirect('/result')

# TEST ROUTE – laat laatste 5 persona's zien
@app.route('/test-db')
def test_db():
    personas = Persona.query.order_by(Persona.id.desc()).limit(5).all()
    return render_template('test_db.html', personas=personas)

# -----------------------------
# RESULT – toon persona
@app.route('/result')
def result():
    persona = session.get('persona')
    if not persona:
        return redirect('/stap1')
    return render_template('result.html', persona=persona)

# -----------------------------
# EXTRA – alle opgeslagen persona’s
@app.route('/personas')
def personas():
    personas = Persona.query.all()
    return render_template('personas.html', personas=personas)

# -----------------------------
# RUN SERVER
if __name__ == '__main__':
    app.run(debug=True)
