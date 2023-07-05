from flask import Flask, flash, redirect, request, url_for, jsonify 
from flask import render_template
from flask import g
from flask import abort
from flask import session
from flask_bootstrap import Bootstrap
from Noticia import Noticia

from SubirNoticia import SubirNoticia
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from ModificarNoticia import Modificar

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

@app.route('/gestion')
def gestion():
    noticias = Noticia.query.all()
    return render_template('gestion.html',noticias=noticias)

@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id):
    modificar = Modificar()

    noticia_a_modificar = Noticia.query.get_or_404(id)

    if request.method == 'POST':
        if modificar.validate_on_submit():

            noticia_a_modificar.titulo    = modificar.titulo.data
            noticia_a_modificar.imagen    = modificar.imagen.data
            noticia_a_modificar.subtitulo = modificar.subtitulo.data
            noticia_a_modificar.resaltado = modificar.resaltado.data
            noticia_a_modificar.columna1  = modificar.columna1.data
            noticia_a_modificar.columna2  = modificar.columna2.data
            noticia_a_modificar.categoria = modificar.categoria.data
            
            db.session.add(noticia_a_modificar)
            db.session.commit()

            flash(f"Noticia '{noticia_a_modificar.titulo}' modificada exitosamente.")
            return redirect("../noticias/" + str(noticia_a_modificar.id))
        else:
            flash("Los datos enviados no son válidos. Revisar el formulario.")
    
    modificar.titulo.data    = noticia_a_modificar.titulo
    modificar.imagen.data    = noticia_a_modificar.imagen
    modificar.subtitulo.data = noticia_a_modificar.subtitulo
    modificar.resaltado.data = noticia_a_modificar.resaltado
    modificar.columna1.data  = noticia_a_modificar.columna1
    modificar.columna2.data  = noticia_a_modificar.columna2
    modificar.categoria.data = noticia_a_modificar.categoria

    return render_template("modificar-noticia.html", form=modificar, noticia_a_modificar=noticia_a_modificar)

@app.route('/eliminar/<int:id>', methods=['DELETE'])
def eliminar(id):
    if request.method == 'DELETE':

        noticia = Noticia.query.get_or_404(id)
        if not noticia:
            return jsonify({'noexiste': f'Error. Noticia de ID {id} inexistente'}), 404
        
        titulo = noticia.titulo
        db.session.delete(noticia)
        db.session.commit()

        return jsonify({'exito': f'Noticia "{titulo}" ha sido eliminada.'}), 200
    else:
        return jsonify({'errordemetodo': 'Método no permitido'}), 405

app.run(debug=True)
