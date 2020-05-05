import pygame, sys
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

import random

# constants & resources
WIDTH = 800
HEIGHT = 600

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

FPS = 60
BALL_SPEED = 10
PADDLE_SPEED = 10

# initialise pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()


class Ball():
    def __init__(self, start_point:tuple, velocity, radius, color):
        self.x = start_point[0]
        self.y = start_point[1]

        if type(velocity) == 'tuple':
            self.v_x = velocity[0]
            self.v_y = velocity[1]
        else:
            self.v_x = self.v_y = velocity

        self.radius = radius
        self.color = color
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    
    def handleBorderCollision(self, width, height):
        if (self.x + self.radius >= width):
            self.v_x *= -1
            self.x = width - self.radius
        elif (self.x - self.radius <= 0):
            self.v_x *= -1
            self.x = self.radius
            

        if (self.y + self.radius >= height):
            self.v_y *= -1
            self.y = height - self.radius
        elif (self.y - self.radius <= 0):
            self.v_y *= -1
            self.y = self.radius
    
    def move(self):
        self.x += self.v_x
        self.y += self.v_y


class Paddle():
    def __init__(self, start_point:tuple, dimension:tuple, color):
        self.x = start_point[0]
        self.y = start_point[1]
        self.breadth = dimension[0]
        self.length = dimension[1]
        self.color = color

    def draw(self, screen):
        rect = pygame.Rect(self.x, self.y, self.breadth, self.length)
        pygame.draw.rect(screen, self.color, rect)

    def move(self, unit):
        self.y += unit
    
    def handleBorderCollision(self, width, height):
        if self.y < 0:
            self.y = 0
        if self.y + self.length > height:
            self.y = height - self.length


def handleCollision(ball, paddle):
    if (ball.x - ball.radius) > (paddle.x + paddle.breadth) + 2:
        return 0
    
    ball_bottom_y = ball.y + ball.radius
    ball_top_y = ball.y - ball.radius

    collided = False

    if (ball_bottom_y > paddle.y) and (ball_bottom_y < paddle.y + paddle.length):
        collided = True
    elif((ball_top_y > paddle.y) and (ball_top_y < paddle.y + paddle.length)):
        collided = True

    if collided:
        x_side = paddle.x + paddle.breadth - ball.x
        y_side = min(ball_bottom_y - paddle.y, paddle.y + paddle.length - ball_top_y)
        
        if(x_side >= y_side):
            ball.v_y *= -1

        if(y_side >= x_side):
            ball.v_x *= -1
            ball.x = paddle.x + paddle.breadth + ball.radius

        return 1

class Player():
    def __init__(self):
        pass
    
    def score(self, score):
        self.score = score
    
    def analyse(self, data):
        pass

def startGame():
    running = True
    lost = False
    score = 0

    start_x = random.randint(WIDTH//2, WIDTH//1.333)
    start_y = random.randint(HEIGHT//4, HEIGHT//1.333)

    ball = Ball((start_x, start_y), BALL_SPEED, 20, BLACK)
    paddle = Paddle((100, random.randint(HEIGHT//3, HEIGHT//1.5)), (20, 100), BLACK)
    player = Player()

    while running:
        screen.fill(WHITE)
        key_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():

            if event.type == QUIT:
                running = False

        # ball logic
        ball.handleBorderCollision(WIDTH, HEIGHT)
        ball.move()
        
        # paddle logic
        data = {'ball_x': ball.x, 'ball_y': ball.y, 'ball_v_x': ball.v_x, 'ball_v_y': ball.v_y, 'pad_y': paddle.y}

        decision = player.analyse(data)
        paddle.move(decision * PADDLE_SPEED) # 0 - stop, 1 - move down, -1 - move up
        paddle.handleBorderCollision(WIDTH, HEIGHT)
        
        # handle collision between ball and paddle
        score += handleCollision(ball, paddle)

        ball.draw(screen)
        paddle.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

        if ball.x < ball.radius + 5:
            lost = True

        if lost:
            player.score(score)


startGame()