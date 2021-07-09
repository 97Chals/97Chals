import turtle
import time
import random
import pickle

"""
reverse shell por TCP
"""
retraso = 0.1

#marcador
score = 0
high_score = 0

#Cola de la serpiente
segmentos = []

#Ventana
wn = turtle.Screen()
wn.title("Snake")
wn.bgcolor("grey")
wn.setup(width=560, height=560)
wn.tracer(0)

#Borde
turtle.shapesize(25,25,5)
turtle.resizemode("user")
turtle.shape("square")

#Cabeza
cabeza = turtle.Turtle()
cabeza.speed(0)
cabeza.shape("square")
cabeza.color("green")
cabeza.penup()
cabeza.goto(0, 0)
cabeza.direction = "stop"


#comida
comida = turtle.Turtle()
comida.speed(0)
comida.shape("circle")
comida.color("red")
comida.penup()
x = random.randint(-230, 230)
y = random.randint(-230, 230)
comida.goto(x, y)
comida.direction = "stop"

#marcador
texto = turtle.Turtle()
texto.speed(0)
texto.color("white")
texto.penup()
texto.hideturtle()
texto.goto(0,250)
#cargar la puntuacion maxima
hs = open("highScore.archivo",'rb')
high_score = pickle.load(hs)
hs.close()

texto.write("Score:{}     High Score:{}".format(score, high_score), align="center", font=("courier", 20, "normal"))

def marcador(score, high_score):
    texto.clear()
    texto.write("Score:{}    High Score:{}".format(score, high_score), align="center", font=("courier", 20, "normal"))

#Deberia guardar en un archivo la puntuacion maxima hecha
def guardarHighScore(high_score):
    hs = open("highScore.archivo", 'rb')
    aux = pickle.load(hs)

    hs.close()
    if high_score > aux:
        hs = open("highScore.archivo",'wb')
        pickle.dump(high_score,hs)
        hs.close()

def leerHighScore():
    hs = open("highScore.archivo",'rb')
    high_score = pickle.load(hs)

    hs.close()

#funciones de movimiento
def mov():
    if cabeza.direction == "up":
        y = cabeza.ycor()
        cabeza.sety(y + 20)
    if cabeza.direction == "down":
        y = cabeza.ycor()
        cabeza.sety(y - 20)
    if cabeza.direction == "left":
        x = cabeza.xcor()
        cabeza.setx(x - 20)
    if cabeza.direction == "right":
        x = cabeza.xcor()
        cabeza.setx(x + 20)

def arriba():
    cabeza.direction = "up"

def abajo():
    cabeza.direction = "down"

def izquierda():
    cabeza.direction = "left"

def derecha():
    cabeza.direction = "right"

#comida
def comer():
    x = random.randint(-230, 230)
    y = random.randint(-230, 230)
    comida.goto(x, y)

    cola()

def cola():
    cola = turtle.Turtle()
    cola.speed(0)
    cola.shape("square")
    cola.color("green")
    cola.penup()
    cola.goto(0, 0)
    cola.direction = "stop"

    #agregar los fragmentos de la cola a la lista
    segmentos.append(cola)

#Movimiento de la cola
def movCola():
    totalSeg = len(segmentos)

    for i in range(totalSeg - 1, 0, -1):
        x = segmentos[i - 1].xcor()
        y = segmentos[i - 1].ycor()
        segmentos[i].goto(x, y)
    if totalSeg > 0:
        x = cabeza.xcor()
        y = cabeza.ycor()
        segmentos[0].goto(x, y)

#colision con los bordes
def colision(high_score):
    #guarda la puntuacion maxima
    guardarHighScore(high_score)

    time.sleep(1)
    cabeza.goto(0, 0)
    cabeza.direction = "stop"

    #esconder la cola
    for cola in segmentos:
        cola.goto(2000,2000)
    #limpiar lista de segmentos
    segmentos.clear()


#Teclado
wn.listen()
wn.onkeypress(arriba, "Up")
wn.onkeypress(abajo, "Down")
wn.onkeypress(izquierda, "Left")
wn.onkeypress(derecha, "Right")

while True:
    wn.update()

    #movimiento de la comida
    if cabeza.distance(comida) < 20:
        comer()
        # aumento de puntuacion
        score += 15

        if score > high_score:
            high_score = score
        marcador(score, high_score)

    #mover cuerpo de la serpiente
    movCola()

    #colision con el borde
    if cabeza.xcor() > 230 or cabeza.ycor() > 230 or cabeza.xcor() < -230 or cabeza.ycor() < -230:
        colision(high_score)
        # reset de marcador
        score = 0
        marcador(score, high_score)

    mov()

    #colision con el cuerpo
    for c in segmentos:
        if c.distance(cabeza) < 20:
            colision(high_score)
            # reset de marcador
            score = 0
            marcador(score, high_score)

    time.sleep(retraso)