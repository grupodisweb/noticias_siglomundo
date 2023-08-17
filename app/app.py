from flask import Flask, flash, redirect, request, url_for, jsonify 
from flask import render_template
from flask import g
from flask import abort
from flask import session
from flask_bootstrap import Bootstrap
from Noticia import Noticia
from Sesion import SesionForm
import os

from SubirNoticia import SubirNoticia
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from ModificarNoticia import Modificar
from Registro import RegistroForm
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import *
from ModificarUsuario import ModificarUsuario

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'laspatatassonhechasconquesodepapas'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///noticias_data_base.db'
login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


class Categoria(db.Model):
    __tablename__ = "Categorías"
    id = db.Column(db.Integer, primary_key=True)
    nombre_interno = db.Column(db.String(20), unique=True)
    nombre_impreso = db.Column(db.String(20), unique=True)

class Imagen(db.Model):
    __tablename__ = "Imágenes"
    id = db.Column(db.Integer, primary_key=True)
    directorio = db.Column(db.String(500), unique=True)

class Noticia(db.Model):
    __tablename__ = "Noticias"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    imagen = db.Column(db.String(500), nullable=False)
    subtitulo = db.Column(db.String(500), nullable=False)
    resaltado = db.Column(db.String(1000), nullable=False)
    columna1 = db.Column(db.String(3000), nullable=False)
    columna2 = db.Column(db.String(3000), nullable=False)
    categoria = db.Column(db.String(20), nullable=False)

class Usuario(UserMixin, db.Model):
    __tablename__ = "Usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(60), unique=True)
    codigo = db.Column(db.String(128), nullable=False) 
    email = db.Column(db.String(150), unique=True)
    rol = db.Column(db.Integer, nullable=False)
    biografia = db.Column(db.String(5000), nullable=True)
    fotoperfil = db.Column(db.String(128), nullable=True)
    titulo = db.Column(db.String(256), nullable=True)

    @property
    def password(self):
        return AttributeError("La contraseña no es visible")
    @password.setter
    def password(self, password):
        self.codigo = generate_password_hash(password)
    def checkPassword(self, password):
        return check_password_hash(self.codigo, password) #es asi?


with app.app_context():
    db.create_all()


def updateImg():
    imagenes = Imagen.query.all()
    lista = []
    for imagen in imagenes:
        lista.append(imagen.directorio)
    for archivo in os.listdir("static/img"):
        if archivo not in lista:
            print(archivo)
            nueva = Imagen(directorio=str(archivo))
            db.session.add(nueva)
            db.session.commit()

def getImages():
    imagenes = Imagen.query.all()
    imagenes_lista = [(i.directorio,i.directorio) for i in imagenes]
    return imagenes_lista

def getCategorias():
    categorias = Categoria.query.all()
    categorias_lista = [(i.nombre_interno,i.nombre_impreso) for i in categorias]
    return categorias_lista

def resumirSubtitulo(noticia):
    i = 0
    maximoPalabras = 12
    resumido = ''
    for caracter in noticia.subtitulo:
        if (caracter == ' '):
            i +=1
        if (i <= maximoPalabras):
            resumido += caracter
        if (i > maximoPalabras):
            break

    return resumido

app.jinja_env.globals.update(resumirSubtitulo=resumirSubtitulo)
app.jinja_env.globals.update(updateImg=updateImg)
app.jinja_env.globals.update(getImages=getImages)
app.jinja_env.globals.update(getCategorias=getCategorias)
# POR HACER: crear más noticias coherentes o agregar noticias reales
#            añadir noticias generales y de tecnología
#            añadirle a las noticias y categorias las columnas

# categorias: "deportes", "misterios", "general", "tecnologia", "internacional"

# nombreDeNoticia = Noticia("Título","/img/Imagen","Subtítulo","Frase Resaltada","Columna Isquierda(no me anda la letra seta :/ )","Columna Derecha","categoría (asegurate que sea una de las cuatro de ahí arriba, si no va a dar error)")

@app.route('/')
def index():
    tamano = db.session.query(Noticia).count()+1
    noticias = Noticia.query.all()
    destacada = Noticia.query.filter_by(titulo="Argentina, Campeón del Mundo").first()
    lista_ultimas = []
    for noticia in noticias:
        if noticia.id >= (tamano - 4):
            lista_ultimas.append(noticia)
        
    return render_template('index.html', noticias=lista_ultimas, tamano=tamano, destacada=destacada)

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

@app.route("/conocenos/")
def conocenos():
    devs = []
    usuarios = Usuario.query.all()
    for usuario in usuarios:
        if (usuario.nombre_usuario == "diego" or usuario.nombre_usuario == "fernando"):
            devs.append(usuario)
    if not devs:
        return abort(404)
    return render_template("conocenos.html", devs=devs) 

@app.route("/inicio-sesion", methods=['POST','GET'])
def inicio_sesion():
    form = SesionForm() 
    if request.method == 'POST':
        if form.validate_on_submit():
            usuario = Usuario.query.filter_by(nombre_usuario=form.nombre.data).first()
            if (usuario):
                if usuario.checkPassword(form.codigo.data): #
                    login_user(usuario)
                    flash('Inicio sesión exitoso.')
                    return redirect('../')
                else:
                    flash('Contraseña incorrecta')
            else:
                flash('Error. Usuario inexistente.')
        else:
            flash('Error. Datos inválidos.')
            
    return render_template('inicio-sesion.html', form=form)
@app.route('/cerrar_sesion')
def cerrar_sesion():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('index'))
@app.route('/cargar-noticias', methods=['GET', 'POST'])
def cargarNoticias():
    updateImg()
    if not current_user.is_authenticated or current_user.rol != 'administrador':
        flash('Error. No tiene permisos')
        return redirect(url_for('inicio_sesion'))
    form = SubirNoticia()
    form.imagen.choices = getImages()
    form.categoria.choices = getCategorias()
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
        texto="Formulario de Subida"
        return render_template('subir-noticia.html', form=form, texto_importante=texto)

@app.route('/gestion')
def gestion():
    if not current_user.is_authenticated or current_user.rol != 'administrador':
        flash('Error. No tiene permisos')
        return redirect(url_for('inicio_sesion'))
    noticias = Noticia.query.all()
    return render_template('gestion.html',noticias=noticias)

@app.route('/usuario/<nombre>', methods=['GET', 'POST'])
def usuario(nombre):
    if not current_user.is_authenticated:
        return redirect(url_for('inicio_sesion'))
    usuario_a_modificar = Usuario.query.filter_by(nombre_usuario=nombre).first()

    return render_template('usuario.html', usuario=usuario_a_modificar)

@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id):
    if not current_user.is_authenticated or current_user.rol != 'administrador':
        flash('Error. No tiene permisos')
        return redirect(url_for('inicio_sesion'))
    modificar = Modificar()

    noticia_a_modificar = Noticia.query.get_or_404(id)
    modificar.imagen.choices = getImages()
    modificar.categoria.choices = getCategorias()
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
    texto="Formulario de Modificación"
    return render_template("modificar-noticia.html", form=modificar, noticia_a_modificar=noticia_a_modificar, texto_importante=texto)

@app.route('/eliminar/<int:id>', methods=['DELETE'])
def eliminar(id):
    if not current_user.is_authenticated or current_user.rol != 'administrador':
        flash('Error. No tiene permisos')
        return redirect(url_for('inicio_sesion'))
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

@app.route('/registro', methods=['POST','GET'])
def registro():
    registrarse = RegistroForm()
    if request.method == 'POST':
        if registrarse.validate_on_submit():
            if (registrarse.nombre.data == 'admin1'):
                rol = 'administrador'
            else: 
                rol = 'normal' 
            usuario_nuevo = Usuario(nombre_usuario=registrarse.nombre.data,password=registrarse.codigo.data,email=registrarse.email.data, rol=rol)
            db.session.add(usuario_nuevo)
            db.session.commit() 
            return redirect('/')
        else:
            flash("Los datos enviados no son válidos. Revisar el formulario.")
    return render_template('registro.html', form=registrarse)

@app.route('/modificar-usuario/<nombre>', methods=['GET', 'POST'])
def modificarUsuario(nombre):
    if not current_user.is_authenticated or current_user.nombre_usuario != nombre:
        flash('Error. No tiene permisos')
        return redirect(url_for('inicio_sesion'))
    modificar = ModificarUsuario()

    usuario_a_modificar = Usuario.query.filter_by(nombre_usuario=nombre).first()
    modificar.fotoperfil.choices = getImages()
    if request.method == 'POST':
        if modificar.validate_on_submit():

            usuario_a_modificar.fotoperfil = modificar.fotoperfil.data
            usuario_a_modificar.titulo     = modificar.tituloperfil.data
            usuario_a_modificar.biografia  = modificar.biografia.data
            
            db.session.add(usuario_a_modificar)
            db.session.commit()

            flash(f"Usuario '{usuario_a_modificar.nombre_usuario}' modificado exitosamente.")
            return redirect("../usuario/" + str(usuario_a_modificar.nombre_usuario))
        else:
            flash("Los datos enviados no son válidos. Revisar el formulario.")
    
    modificar.biografia.data            = usuario_a_modificar.biografia
    modificar.fotoperfil.data           = usuario_a_modificar.fotoperfil
    modificar.tituloperfil.data         = usuario_a_modificar.titulo
    return render_template("modificar-usuario.html", form=modificar, usuario=usuario_a_modificar)

app.run(debug=True)
