from flask import Flask, flash, redirect, request, url_for 
from flask import render_template
from flask import g
from flask import abort
from flask import session
from flask_bootstrap import Bootstrap
from Noticia import Noticia

from SubirNoticia import SubirNoticia
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'laspatatassonhechasconquesodepapas'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///noticias_data_base.db'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Noticia(db.Model):
    __tablename__ = "Noticias"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False)
    imagen = db.Column(db.String(120), nullable=False)
    subtitulo = db.Column(db.String(300), nullable=False)
    resaltado = db.Column(db.String(500), nullable=False)
    columna1 = db.Column(db.String(2000), nullable=False)
    columna2 = db.Column(db.String(2000), nullable=False)
    categoria = db.Column(db.String(16), nullable=False)


with app.app_context():
    db.create_all()



def resumirSubtitulo(noticia):
    i = 0
    resumido = ''
    for caracter in noticia.subtitulo:
        i +=1
        if (i < 51):
            resumido += caracter
    return resumido

app.jinja_env.globals.update(resumirSubtitulo=resumirSubtitulo)
# POR HACER: crear más noticias coherentes o agregar noticias reales
#            añadir noticias generales y de tecnología
#            añadirle a las noticias y categorias las columnas

# categorias: "deportes", "misterios", "general", "tecnologia", "internacional"

# nombreDeNoticia = Noticia("Título","/img/Imagen","Subtítulo","Frase Resaltada","Columna Isquierda(no me anda la letra seta :/ )","Columna Derecha","categoría (asegurate que sea una de las cuatro de ahí arriba, si no va a dar error)")

@app.route('/')
def index():
    tamano = db.session.query(Noticia).count()+1
    noticias = Noticia.query.all()
    lista_ultimas = []
    for noticia in noticias:
        if noticia.id >= (tamano - 4):
            lista_ultimas.append(noticia)
        
    return render_template('index.html', noticias=lista_ultimas, tamano=tamano)

@app.route("/noticias/<int:id>")
def ir_a_noticia(id):
    noticias = Noticia.query.all()
    # Buscamos el alumno por padrón, devolvemos None si el mismo no se encuentra
    noticia_buscada = next((noticia for noticia in noticias if noticia.id == id), None)
    if not noticia_buscada:
        return abort(404)
    return render_template("noticia-base.html", noticia_buscada=noticia_buscada, noticias=noticias)
@app.route("/categorias/<categoria>")
def ir_a_categoria(categoria):
    noticias_en_categoria = []
    noticias = Noticia.query.all()
    for noticia in noticias:
        if (noticia.categoria == categoria):
            noticias_en_categoria.append(noticia)
    if not noticias_en_categoria:
        return abort(404)
    return render_template("categorias-base.html", noticias=noticias_en_categoria)  

@app.route("/inicio-sesion")
def inicio_sesion():
    return render_template('inicio-sesion.html')

@app.route('/cargar-noticias', methods=['GET', 'POST'])
def cargarNoticias():
    form = SubirNoticia()
    if request.method == 'POST':
        if form.validate_on_submit():
            nuevaNoticia = Noticia(titulo=form.titulo.data, imagen=form.imagen.data, subtitulo=form.subtitulo.data, resaltado=form.resaltado.data, columna1=form.columna1.data, columna2=form.columna2.data, categoria=form.categoria.data)
            db.session.add(nuevaNoticia)
            db.session.commit()
            form.titulo.data = ''
            form.imagen.data = ''
            form.subtitulo.data = ''
            form.resaltado.data = ''
            form.columna1.data = ''
            form.columna2.data = ''
            form.categoria.data = ''
            return redirect("noticias/" + str(nuevaNoticia.id))
        return flash("Datos de formulario incorrectos.")
    else:   
        return render_template('subir-noticia.html', form=form)

app.run(debug=True)
