from flask import Flask

app = Flask(__name__)

# Clave secreta necesaria para utilizar session y flash messages de manera segura
app.secret_key = "esta_es_una_clave_secreta_muy_segura"