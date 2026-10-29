from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['POST'])
def registro():
    if not Usuario.validar_registro(request.form):
        return redirect('/')

    password_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "password": password_hash
    }

    user_id = Usuario.guardar(data)
    session['user_id'] = user_id
    session['usuario_nombre'] = request.form['nombre']

    return redirect('/success')

@app.route('/login', methods=['POST'])
def login():
    usuario_db = Usuario.obtener_por_email(request.form['email'])
    if not usuario_db:
        flash("Correo o contraseña incorrectos.", "login")
        return redirect('/')

    if not bcrypt.check_password_hash(usuario_db.password, request.form['password']):
        flash("Correo o contraseña incorrectos.", "login")
        return redirect('/')

    session['user_id'] = usuario_db.id
    session['usuario_nombre'] = usuario_db.nombre

    return redirect('/success')

@app.route('/success')
def success():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('inicio.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
