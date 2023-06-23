from flask import Flask, flash, redirect, request, url_for 
from flask import render_template
from flask import g
from flask import abort
from flask import session
from flask_bootstrap import Bootstrap

from Noticia import Noticia
from SubirNoticia import SubirNoticia

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'laspatatassonhechasconquesodepapas'

# POR HACER: crear más noticias coherentes o agregar noticias reales
#            añadir noticias generales y de tecnología
#            añadirle a las noticias y categorias las columnas

# categorias: "deportes", "misterios", "general", "tecnologia"

# nombreDeNoticia = Noticia("Título","/img/Imagen","Subtítulo","Frase Resaltada","Columna Isquierda(no me anda la letra seta :/ )","Columna Derecha","categoría (asegurate que sea una de las cuatro de ahí arriba, si no va a dar error)")
noticia5 = Noticia("El Abuelo de la Empanada Murió", "/img/tablero-didactico.jpg", "Fue asesinado a sangre fría por la hermanastra del amigo de su nieto, usando un tateti envenenado.", "Sus huellas fueron encontradas en el tablero.", "Se dice que queria robar el tesoro familiar de la empanada parlante alienigena, sin suerte, pues la misma la llevo a la comisaria. El plan que tenia pareceria impecable a cualquiera, mas el conocimiento de la empanada alienigena la supero.", "Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsum aperiam recusandae nostrum commodi quis nesciunt culpa delectus, officia expedita temporibus eveniet ullam enim non natus deleniti adipisci eius libero neque!", "misterios" )
noticia4 = Noticia("Invasión de nueva especie", "/img/pradera.jpg", "Una nueva especie de perrito de las praderas fue encontrado.","Granjeros alrededor del mundo pierden el sueño ante esta peligrosa especie.","Puede cambiar la forma de sus dientes para roer cualquier material, aunque le toma algunos dias adaptarse, granjeros alrededor del mundo estan asustados que esto podria arruinar sus cosechas para siempre","Parece salida de una película, o de un videojuego, pero esta especie es definitivamente, absolutamente real y nadie sabe de dónde salió ni cómo detenerla. Algunos científicos tienen la teoría de que son en realidad alienígenas invasores, pues el ADN de estas criaturas no se parece a nada visto anteriormente.", "misterios" )
noticia3 = Noticia("Un Desmayo Inesperado", "/img/nadadora.webp", "La nadadora artística estadounidense Anita Alvarez, sufrió un desmayo.","Por suerte, fue salvada por su entrenadora.", "No ha sido autorizada para la competición por equipos, prueba que se desarrolla el viernes en los Mundiales de Budapest, según la lista de participantes actualizada. Alvarez, que perdió el conocimiento al final de su ejercicio individual, figuraba en todas las listas precedentes del equipo estadounidense, pero ha sido remplazada por Yujin Chang poco antes del inicio de la prueba. “Es una decisión tomada por la FINA”, declaró Selina Shah, médica del equipo estadounidense de natación artística. “Desde mi punto de vista, ella habría podido participar”, añadió.", "La nadadora de 25 años fue rescatada por su entrenadora, la española Andrea Fuentes, que se tiró al agua vestida con pantalón corto y camiseta, para lograr sacarla a la superficie con sus brazos. ”Creo que estuvo al menos dos minutos sin respirar porque sus pulmones estaban llenos de agua”, contó más tarde la entrenadora. Alvarez ha tenido que pasar un examen médico completo el viernes por la mañana, Luego de eso, se conoció la noticia de que Alvarez no participaría de la competencia.", "deportes" )
noticia2 = Noticia("Golfista Trotamundos", "/img/nadadora.webp", "El US Open es un major cada vez más generoso. Este año alcanzó un nuevo récord: 10.187 golfistas", "Ellos intentaron clasificarse para conseguir una de las 64 plazas disponibles.", "El certamen arranca este jueves en The Los Angeles Country Club, en Beverly Hills. Y entre ese ejército de aspirantes, siempre trasciende alguna historia curiosa, digna de ser contada. En este caso, la gran atracción entre los jugadores “humildes” confirmados en el field es Berry Henson, un chofer de Uber que realizó unos 3000 viajes y ostenta una calificación al volante que habla de su eficiencia y trato cordial: 4,99 puntos. Henson, de 43 años, es un buscavidas del golf que, cuando le preguntaron hasta qué punto vivió como un trotamundos en este deporte,", "se encargó de enumerar la cantidad de circuitos de los que formó parte para intentar ganarse unos dólares aquí y allá. La lista de tours toca casi todos los puntos del planeta: PGA Tour -solo jugó tres certámenes-, DP World Tour, Korn Ferry Tour, Challenge Tour, Asian Tour, Japan Tour, Korean Tour, Sunshine Tour, Canadian Tour, Hooters Tour, eGolf Tour, Golden State Tour, Pepsi Tour, National Pro Tour y algunos más que seguramente ya olvidó. “A lo largo de dos décadas, creo que la única gira en la que no estuve fue la del PGA Tour Latinoamérica”, comenta.", "deportes" )
noticia1 = Noticia("Una Partida para la Historia", "/img/tablero-didactico.jpg", "Esta partida del tateti duró 7.536 años. El porqué te impresionará.", "'¡Ajá! ¡Después de tantos años, este es mi momento!'- dijo un jugador.", "Esta legendaria partida duró tantos años porque fue una partida entre dos seres de otro planeta, que tienen ciclos de vida 1.000 veces más largos, por lo que, para nosotros, se mueven muy lento." , "Sin embargo, y con mucha suerte, sus pensamientos son transmitidos en un radio de 10 metros al rededor de ellos, y fuimos capaces de entender lo que uno decía: '¡Ajá! ¡Después de tantos años, este es mi momento!'. Irónicamente, nada más lo pensó, fue derrotado de forma humillante.", "general")
noticia6 = Noticia("Argentina, campeón del mundo", "/img/argentinacampeon.jpg", "Argentina, campeón del mundo: de la mano de Messi y Dibu, le ganó a Francia y consiguió su tercera estrella ⭐⭐⭐", "La selección argentina de fútbol se proclamó por tercera vez en su historia campeona del mundo: '¡La c*** de tu madre, somos campeones del mundo!'", "(18.12.2022) en Qatar, minutos después de ganar su primera Copa del Mundo, un Lionel Messi en éxtasis tomó el micrófono del Estadio de Lusail: '¡La c*** de tu madre, somos campeones del mundo!'\nEl astro saludó con esa frase tan argentina, no exenta de connotaciones negativas, a los miles de hinchas de la Albiceleste que ondeaban camisetas y celebraban el título del equipo de Lionel Scaloni. Messi, con siete goles y tres asistencias a lo largo del torneo, fue elegido como el mejor jugador de la final y también del Mundial 2022,", "secundado en los premios individuales por sus compatriotas Enzo Fernández, el mejor joven, y Emiliano Martínez, mejor portero.\nEl francés Kylian Mbappé fue reconcido como el mejor goleador, con ocho dianas. No solo se llevó la Bota de Oro, sino el récord de máximo goleador en una final. Además, desde 2002, con Ronaldo Nazario con Brasil, nadie alcanzaba ocho goles en la fase final de la competición. Sin embargo, estaba abatido tras el final del partido, en el que metió tres goles, además de otro más en la tanda de penales. El propio presidente francés, Emmanuel Macron, bajó al terreno de juego para consolar a la selección y, en especial, a un Mbappé sentado sobre el césped y con la cabeza baja.", "deportes" )
noticias = [noticia1, noticia2, noticia3, noticia4, noticia5, noticia6]
@app.before_request
def obtener_noticias():
    g.lista_noticias = noticias

@app.route('/')
def index():
    # for noticia in noticias:
    #     ultima_noticia = noticia
    tamaño = len(noticias) - 1
    return render_template('index.html', tamaño=tamaño, noticias=noticias)

@app.route("/noticias/<int:id>")
def ir_a_noticia(id):
    # Buscamos el alumno por padrón, devolvemos None si el mismo no se encuentra
    noticia_buscada = next((noticia for noticia in g.lista_noticias if noticia.id == id), None)
    if not noticia_buscada:
        return abort(404)
    return render_template("noticia-base.html", noticia_buscada=noticia_buscada, noticias=noticias)
@app.route("/categorias/<categoria>")
def ir_a_categoria(categoria):
    noticias_en_categoria = []
    for noticia in g.lista_noticias:
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
            nuevaNoticia = Noticia(form.titulo.data, form.imagen.data, form.subtitulo.data, form.resaltado.data, form.columna1.data, form.columna2.data, form.categoria.data)
            noticias.append(nuevaNoticia)
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
