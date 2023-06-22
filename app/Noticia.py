import random


class Noticia:
    
    id = 0

    def __init__(self, titulo, imagen, subtitulo, resaltado, columna1, columna2, categoria):
        self.id = self.obtenerNuevoID()
        self.titulo = titulo
        self.imagen = imagen
        self.subtitulo = subtitulo
        self.resaltado = resaltado
        self.columna1 = columna1
        self.columna2 = columna2
        self.categoria = categoria

    def obtenerNuevoID(cls):
        cls.id += (random.randint(1,100) % 100)
        return cls.id

    def obtenerIDParaImprimir(self):
        idlength = len(self.id)
        if (idlength == 1):
            return "000" + str(self.id)
        elif (idlength == 2):
            return "00" + str(self.id)
        elif (idlength == 3):
            return "0" + str(self.id)
        elif (idlength == 4):
            return str(self.id)
        else:
            return "Error. El ID no puede ser vacío."

    def obtenerImagen(self):
        return f"../static{self.imagen}"

    def resumirSubtitulo(self):
        i = 0
        resumido = ''
        for caracter in self.subtitulo:
            i +=1
            if (i < 51):
                resumido += caracter
        return resumido
