from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

# Expresión regular para validar el formato del correo electrónico
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.update_at = data['update_at']

    @classmethod
    def guardar(cls, formulario):
        query = "INSERT INTO usuarios (nombre, apellido, email, password, created_at, update_at) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('mydb').query_db(query, formulario)

    @classmethod
    def obtener_por_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL('mydb').query_db(query, {'email': email})
        if len(resultado) < 1:
            return None
        return cls(resultado[0])

    @classmethod
    def obtener_por_id(cls, usuario_id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        resultado = connectToMySQL('mydb').query_db(query, {'id': usuario_id})
        if len(resultado) < 1:
            return None
        return cls(resultado[0])

    @staticmethod
    def validar_registro(formulario):
        es_valido = True
        
        # Nombre: solo letras, al menos 2 caracteres
        if len(formulario['nombre']) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "registro")
            es_valido = False
        elif not formulario['nombre'].isalpha():
            flash("El nombre solo debe contener letras.", "registro")
            es_valido = False

        # Apellido: solo letras, al menos 2 caracteres
        if len(formulario['apellido']) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "registro")
            es_valido = False
        elif not formulario['apellido'].isalpha():
            flash("El apellido solo debe contener letras.", "registro")
            es_valido = False

        # E-mail: formato correcto y que no exista previamente
        if not EMAIL_REGEX.match(formulario['email']):
            flash("Formato de correo electrónico inválido.", "registro")
            es_valido = False
        elif Usuario.obtener_por_email(formulario['email']):
            flash("El correo electrónico ya está registrado.", "registro")
            es_valido = False

        # Contraseña: al menos 8 caracteres y coincidencia con la confirmación
        if len(formulario['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "registro")
            es_valido = False
        elif formulario['password'] != formulario['confirm_password']:
            flash("Las contraseñas no coinciden.", "registro")
            es_valido = False

        return es_valido