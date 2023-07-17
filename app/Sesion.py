from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from wtforms.validators import Length
class SesionForm(FlaskForm):
    nombre = StringField("Ingrese su nombre de usuario", validators=[DataRequired(),Length(min=5, max=100,message="El largo del título debe ser mayor a 5 y menor a 50.")])
    codigo = StringField("Ingrese su contraseña", validators=[DataRequired()])
    submit = SubmitField("Ingresar")