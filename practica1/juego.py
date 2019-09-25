import random

class Jugador:
    numeros_propuestos = []
    def __init__(self, nombre = 'IA' ,tipo = 'IA',a = 0, b = 100):
        self.nombre = nombre
        self.tipo = tipo
        self.a = a
        self.b = b
    def pensar(self):
        if self.tipo == 'IA':
            self.numero_pensado = random.randrange(self.a, self.b)
        else:
            print('{}, elige un número entre {} y {}:'.format(self.nombre, self.a, self.b))
            numero = int(input())
            self.numero_pensado = numero
    def proponer(self):
        if self.tipo == 'IA':
            # propone números aleatorios, se podría mejorar utilizando algo similar a una búsqueda dicotómica
            numero = random.randrange(self.a, self.b)
            while numero in self.numeros_propuestos:
                numero = random.randrange(self.a, self.b)
            self.numeros_propuestos.append(numero)
            return numero
        else:
            print('{}, propón un número entre {} y {}:'.format(self.nombre, self.a, self.b))
            numero = int(input())
            while numero in self.numeros_propuestos:
                print('Ya has propuesto ese número, prueba otra vez:')
                numero = int(input())
            self.numeros_propuestos.append(numero)
            return numero
    def comprobar(self, num):
        if num == self.numero_pensado:
            return 0
        elif num < self.numero_pensado:
            return -1
        else:
            return 1

class Partida:
    def __init__(self):
        self.num_intentos = 0
        print('Introduce el número de jugadores (1 o 2)')
        num_jugadores = int(input())
        while (num_jugadores != 1) and (num_jugadores != 2):
            print('Numero de jugadores incorrecto (debe ser 1 o 2), vuelve a introducirlo')
            num_jugadores = int(input())
        if num_jugadores == 1:
            print('Cual es tu nombre?')
            nombre = input()
            print('Quieres ser el jugador 1 o 2?')
            num_jugador = int(input())
            while num_jugador != 1 and num_jugador != 2:
                print('Numero de jugador incorrecto (debe ser 1 o 2), vuelve a introducirlo')
                num_jugador = int(input())
            if num_jugador == 1:
                self.jugador1 = Jugador(nombre,'humano')
                self.jugador2 = Jugador()
            elif num_jugador == 2:
                self.jugador2 = Jugador(nombre, 'humano')
                self.jugador1 = Jugador()
        else:
            print('Jugador1 introduce tu nombre:')
            nombre = input()
            self.jugador1 = Jugador(nombre,'humano')
            print('Jugador2 introduce tu nombre:')
            nombre = input()
            self.jugador2 = Jugador(nombre, 'humano')

if __name__ == '__main__':
    respuesta = 'S'
    while respuesta == 'S':
        print('Comienza el juego')
        partida = Partida()
        j1 = partida.jugador1
        j2 = partida.jugador2
        resultado = 3
        j1.pensar()
        while resultado != 0:
            n_propuesto = j2.proponer()
            partida.num_intentos+=1
            resultado = j1.comprobar(n_propuesto)
            if resultado == 0:
                print('{} ha acertado en {} intento(s)'.format(j2.nombre, partida.num_intentos))
            elif resultado == -1 and j2.tipo != 'IA':
                print('El número pensado es mayor que {}'.format(n_propuesto))
            elif resultado == 1 and j2.tipo != 'IA':
                print('El número pensado es menor que {}'.format(n_propuesto))
        print('¿Quieres seguir jugando? S/N')
        respuesta = input()


