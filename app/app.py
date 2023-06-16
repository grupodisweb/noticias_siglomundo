from flask import Flask, g, render_template
from flask import request

from Alumno import Alumno

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/noticia-campeon")
def noticia_campeon():
    return render_template('noticia-campeon.html')

@app.route("/noticia-perrito")
def noticia_perrito():
    return render_template('noticia-perrito.html')

@app.route("/noticia-abuelo")
def noticia_abuelo():
    return render_template('noticia-abuelo.html')

@app.route("/inicio-sesion")
def inicio_sesion():
    return render_template('inicio-sesion.html')

@app.route("/noticia-nadadora")
def nadadora():
    return render_template('noticia-nadadora.html')

@app.route("/categoria-deportes")
def deportes():
    return render_template('categoria-deportes.html')

app.run(debug=True)
