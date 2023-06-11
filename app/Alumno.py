class Alumno:
    # Atributo de clase
    # padron = 0

    def __init__(self, nombre, apellido, padron):
        self.nombre = nombre
        self.apellido = apellido
        self.padron = padron

        # Alumno.incrementarPadron()

    # @classmethod
    # def incrementarPadron(cls):
    #     cls.padron += 1

    def getNombre(self):
        return self.nombre
    
    def getApellido(self):
        return self.apellido

    def getPadron(self):
        return self.padron


