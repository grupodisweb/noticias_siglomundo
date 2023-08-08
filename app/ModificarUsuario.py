from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from wtforms.validators import Length
class ModificarUsuario(FlaskForm):
    tituloperfil = StringField("Ingrese el título de su biografía", validators=[DataRequired(),Length(min=5, max=100,message="El largo del título debe ser mayor a 5 y menor a 50.")])
    fotoperfil = SelectField("Seleccione su foto de perfil:", coerce=str, validators=[DataRequired()])
    biografia = StringField("Ingrese su biografía", validators=[DataRequired()])
    submit = SubmitField("Ingresar")
