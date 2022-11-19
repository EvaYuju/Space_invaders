import sys

import pygame
import random
import math
from pygame import mixer

# Configuración general
pygame.init()  # Inicializa los módulos pygame y es requerido para cualquier tipo de juego
#  reloj = pygame.time.Clock()  # Método reloj

# Creación de ventana (Tamaño, título...)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
# Título ventana:
pygame.display.set_caption("Juego Front Invaders - Equipo 4 PMDM 1T 2ºD.A.M.")

#  Variables de texto para puntuación
score_val = 0
scoreX = 5
scoreY = 5  # (nombre fuente, tamaño)
font = pygame.font.Font("data/Goldman-Regular.ttf", 20)

# Fuente para fin de juego
game_over_font = pygame.font.Font("data/Goldman-Regular.ttf", 64)


def show_score(x, y):
    score = font.render("Points: " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    game_over_text = game_over_font.render("HAS PERDIDO", True, (255, 255, 255))
    screen.blit(game_over_text, (190, 250))


# Background Sound
mixer.music.load('data/background.wav')
mixer.music.play(-1)

# player
playerImage = pygame.image.load('data/spaceship.png')
player_X = 370
player_Y = 523
player_Xchange = 0

# Invader
invaderImage = []
invader_X = []
invader_Y = []
invader_Xchange = []
invader_Ychange = []
no_of_invaders = 8
for num in range(no_of_invaders):
    invaderImage.append(pygame.image.load('data/alien.png'))
    invader_X.append(random.randint(64, 737))
    invader_Y.append(random.randint(30, 180))
    invader_Xchange.append(1.2)
    invader_Ychange.append(50)

# Bullet
# rest - bullet is not moving
# fire - bullet is moving
bulletImage = pygame.image.load('data/bullet.png')
bullet_X = 0
bullet_Y = 500
bullet_Xchange = 0
bullet_Ychange = 3
bullet_state = "rest"


# Collision Concept
def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    if distance <= 50:
        return True
    else:
        return False


def player(x, y):
    screen.blit(playerImage, (x - 16, y + 10))


def invader(x, y, invader):
    screen.blit(invaderImage[invader], (x, y))


def bullet(x, y):
    global bullet_state
    screen.blit(bulletImage, (x, y))
    bullet_state = "fire"


# Bucle (donde ejecutaremos las funciones):
running = True
while running:

    # RGB
    screen.fill((0, 0, 0))
    # zona inputs
    for event in pygame.event.get():  # Llamadas a todos los eventos de usuarios
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  # Cerrar el juego una vez termina

        # Control del movimiento del jugador con los eventos de teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # Pulsar flecha izquierda
                player_Xchange = -1       # Movimiento hacia la izquierda
            if event.key == pygame.K_RIGHT:  # Pulsar flecha derecha
                player_Xchange = 1        # Movimiento hacia la derecha
            if event.key == pygame.K_SPACE:  # Pulsar barra espaciadora
                # Cambio de dirección de la bala.
                if bullet_state == "rest":
                    bullet_X = player_X
                    bullet(bullet_X, bullet_Y)
                    bullet_sound = mixer.Sound('data/bullet.wav')
                    bullet_sound.play()
        if event.type == pygame.KEYUP:
            player_Xchange = 0

    # adding the change in the player position
    player_X += player_Xchange
    for i in range(no_of_invaders):
        invader_X[i] += invader_Xchange[i]

    # bullet movement
    if bullet_Y <= 0:
        bullet_Y = 600
        bullet_state = "rest"
    if bullet_state == "fire":
        bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Ychange

    # movement of the invader
    for i in range(no_of_invaders):

        if invader_Y[i] >= 450:
            if abs(player_X - invader_X[i]) < 80:
                for j in range(no_of_invaders):
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
            score_val += 1
            bullet_Y = 600
            bullet_state = "rest"
            invader_X[i] = random.randint(64, 736)
            invader_Y[i] = random.randint(30, 200)
            invader_Xchange[i] *= -1

        invader(invader_X[i], invader_Y[i], i)

    # restricting the spaceship so that it doesn't go out of screen
    if player_X <= 16:
        player_X = 16
    elif player_X >= 750:
        player_X = 750

    player(player_X, player_Y)
    show_score(scoreX, scoreY)
    pygame.display.update()
    #  reloj.tick(120)  # Reloj para ejecutar el bucle = 60 veces por segundo

