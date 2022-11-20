import sys

import pygame
import random
import math
from pygame import mixer

# Configuración general
pygame.init()  # Inicializa los módulos pygame y es requerido para cualquier tipo de juego
pygame.font.init()  # Inicializa el módulo font para las fuentes
pygame.mixer.pre_init(44100, -16, 2, 512)  # (freq 44100 x defecto, -16 x def, canal2 x def, tamaño buffer lo reducimos)
reloj = pygame.time.Clock()  # Método reloj que usaremos para la velocidad de ejecución del bucle

# Creación de ventana
anchoPantalla = 800 
altoPantalla = 600
pantalla = pygame.display.set_mode((anchoPantalla, altoPantalla))
# Título ventana
pygame.display.set_caption("Juego Front Invaders - Equipo 4 PMDM 1T 2ºD.A.M.")

# Sonido de fondo
mixer.music.load('data/background.wav')
mixer.music.play(-1)

# Variables de texto para puntuación
puntos = 0
marcadorX = 5
marcadorY = 5              # ("path/nombre-fuente", tamaño)
fuente1 = pygame.font.Font("data/Goldman-Regular.ttf", 20)

# Fuente para fin de juego
fuente2 = pygame.font.Font("data/Goldman-Regular.ttf", 64)


# Función para mostrar la puntuación
def marcador(x, y):
    score = fuente1.render("Puntos: " + str(puntos), True, (255, 255, 255))
    pantalla.blit(score, (x, y))


# Función que muestra HAS PERDIDO
def game_over():
    txt_perder = fuente2.render("HAS PERDIDO", True, (255, 255, 255))
    pantalla.blit(txt_perder, (190, 250))


# Configurando el jugador: sprite nave y posición en la pantalla
nave = pygame.image.load('data/spaceship.png')
player_X = 370
player_Y = 523
player_Xchange = 0

# Invader
invaderImage = []
invader_X = []
invader_Y = []
invader_Xchange = []
invader_Ychange = []
numEnemigos = 2
for num in range(numEnemigos):
    invaderImage.append(pygame.image.load('data/alien.png'))
    invader_X.append(random.randint(84, 737))
    invader_Y.append(random.randint(30, 180))
    invader_Xchange.append(1.8)
    invader_Ychange.append(50)

# Disparo
# off - disparo apagado
# on - disparo en movimiento
bulletImage = pygame.image.load('data/bullet.png')
bullet_X = 0
bullet_Y = 500
bullet_Xchange = 0
bullet_Ychange = 3
bullet_state = "off"


# Detector de colisiones
def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    if distance <= 50:
        return True
    else:
        return False


def player(x, y):
    pantalla.blit(nave, (x - 16, y + 10))


def invader(x, y, invader):
    pantalla.blit(invaderImage[invader], (x, y))


def bullet(x, y):
    global bullet_state
    pantalla.blit(bulletImage, (x, y))
    bullet_state = "on"


# Bucle (donde ejecutaremos las funciones):
running = True
while running:

    # RGB
    pantalla.fill((0, 0, 0))
    # zona inputs
    for event in pygame.event.get():  # Llamadas a todos los eventos de usuarios
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  # Cerrar el juego una vez termina

        # Control del movimiento del jugador con los eventos de teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # Pulsar flecha izquierda
                player_Xchange = -1  # Movimiento hacia la izquierda
            if event.key == pygame.K_RIGHT:  # Pulsar flecha derecha
                player_Xchange = 1  # Movimiento hacia la derecha
            if event.key == pygame.K_SPACE:  # Pulsar barra espaciadora
                # Cambio de dirección de la bala.
                if bullet_state == "off":
                    bullet_X = player_X
                    bullet(bullet_X, bullet_Y)
                    bullet_sound = mixer.Sound('data/bullet.wav')
                    bullet_sound.play()
        if event.type == pygame.KEYUP:
            player_Xchange = 0

    # adding the change in the player position
    player_X += player_Xchange
    for i in range(numEnemigos):
        invader_X[i] += invader_Xchange[i]

    # bullet movement
    if bullet_Y <= 0:
        bullet_Y = 600
        bullet_state = "off"
    if bullet_state == "on":
        bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Ychange  # El disparo va hacia arriba

    # Movimiento enemigo
    for i in range(numEnemigos):

        if invader_Y[i] >= 450:
            if abs(player_X - invader_X[i]) < 80:
                for j in range(numEnemigos):
                    invader_Y[j] = 2000
                    explosion_sound = mixer.Sound('data/explosion.wav')
                    explosion_sound.play()
                game_over()
                break

        if invader_X[i] >= 735 or invader_X[i] <= 0:
            invader_Xchange[i] *= -1
            invader_Y[i] += invader_Ychange[i]
        # Collision
        collision = isCollision(bullet_X, invader_X[i], bullet_Y, invader_Y[i])
        if collision:
            puntos += 1
            bullet_Y = 600
            bullet_state = "off"
            invader_X[i] = random.randint(64, 736)
            invader_Y[i] = random.randint(30, 200)
            invader_Xchange[i] *= -1

        invader(invader_X[i], invader_Y[i], i)

    # Condición para la nave espacial para que no se salga de la pantalla
    if player_X <= 16:
        player_X = 16
    elif player_X >= 750:
        player_X = 750

    player(player_X, player_Y)
    marcador(marcadorX, marcadorY)
    pygame.display.update()
    reloj.tick(140)  # Reloj para ejecutar el bucle = 60 veces por segundo
