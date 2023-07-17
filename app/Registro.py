from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, EqualTo
from wtforms.validators import Length
class RegistroForm(FlaskForm):
    nombre = StringField("Ingrese su nombre de usuario", validators=[DataRequired(),Length(min=5, max=100,message="El largo del título debe ser mayor a 5 y menor a 50.")])
    codigo = PasswordField("Ingrese su contraseña", validators=[DataRequired()])
    codigo2 = PasswordField("Confirme su contraseña", validators=[DataRequired(), EqualTo("codigo",message="Las contrasñeas deben coincidir")])
    email = EmailField("Ingrese su email", validators=[DataRequired()])
    email2 = EmailField("Confirme su email", validators=[DataRequired(), EqualTo("email",message="Los emails deben coincidir")])
    submit = SubmitField("Ingresar")