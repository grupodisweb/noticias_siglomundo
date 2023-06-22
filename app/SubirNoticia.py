from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from wtforms.validators import Length
class SubirNoticia(FlaskForm):
    # id = IntegerField("Ingrese el ID de la noticia (5 dígitos)", validators=[DataRequired(),Length(min=5, max=5,message="El ID debe tener 5 dígitos.")])
    titulo = StringField("Ingrese el título de la noticia", validators=[DataRequired(),Length(min=5, max=50,message="El largo del título debe ser mayor a 5 y menor a 50.")])
    imagen = StringField("Ingrese el link directo a una imagen", validators=[DataRequired()])
    subtitulo = StringField("Ingrese un subtitulo", validators=[DataRequired()])
    resaltado = StringField("Ingrese la frase más importante del texto", validators=[DataRequired()])
    columna1 = StringField("Ingrese el texto que irá en la primera columna", validators=[DataRequired()])
    columna2 = StringField("Ingrese el texto que irá en la segunda columna", validators=[DataRequired()])
    categoria = SelectField(choices=[('a', 'deportes'),('b','misterio'),('c','general'),('c', 'tecnologia')], validators=[DataRequired()])
    submit = SubmitField("Ingresar")
