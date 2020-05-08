import pygame
import entity
import random
from entity import Ball, Paddle
from pygame.locals import QUIT
# constants & resources

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

FPS = 240
BALL_SPEED = 20
PADDLE_SPEED = 30

WIDTH = 800
HEIGHT = 500

def startGame(player, screen, clock):
    running = True
    lost = False
    points = 0

    start_x = random.randint(WIDTH//2, WIDTH//1.333)
    start_y = random.randint(HEIGHT//4, HEIGHT//1.333)

    ball = Ball((start_x, start_y), BALL_SPEED, 20, BLACK)
    paddle = Paddle((100, random.randint(HEIGHT//3, HEIGHT//1.5)), (20, 100), BLACK)

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():

            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.quit()

        # ball logic
        lost = ball.handleBorderCollision(WIDTH, HEIGHT)

        if ball.x < 20:
            lost = True

        if lost or points > 20:
            player.score(points)
            return

        ball.move()
        
        # paddle logic
        data = {'ball_x': ball.x, 'ball_y': ball.y, 'ball_v_x': ball.v_x, 'ball_v_y': ball.v_y, 'pad_y': paddle.y}

        decision = player.analyse(data)

        # 1 - move down,  0 - move up, 2 - stays still
        if decision == 0:
            decision = -1
        elif decision == 2:
            decision = 0

        paddle.move(decision * PADDLE_SPEED)
        paddle.handleBorderCollision(WIDTH, HEIGHT)
        
        # handle collision between ball and paddle
        points += entity.handleCollision(ball, paddle)

        ball.draw(screen)
        paddle.draw(screen)
        pygame.display.update()
        clock.tick(FPS)
