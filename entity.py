# Handles the graphics part

import pygame
import random

class Ball:

    def __init__(self, start_point:tuple, velocity, radius, color):
        self.x = start_point[0]
        self.y = start_point[1]

        if type(velocity) == 'tuple':
            self.v_x = velocity[0]
            self.v_y = velocity[1]
        else:
            self.v_x = self.v_y = velocity
        
        # randomise ball y velocity 
        r = random.randint(0,2)
        if r == 0:
            self.v_y *= -1

        self.radius = radius
        self.color = color
    

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    
    def handleBorderCollision(self, width, height):
        r = random.randint(-1,2)

        if (self.x + self.radius >= width):
            self.v_x *= -1
            self.v_x += r
            self.x = width - self.radius
        elif (self.x - self.radius <= 0):
            return True
            # self.v_x *= -1
            # self.x = self.radius
            
        r = random.randint(-1,2)
        if (self.y + self.radius >= height):
            self.v_y *= -1
            self.v_y += r
            self.y = height - self.radius
        elif (self.y - self.radius <= 0):
            self.v_y *= -1
            self.v_y += r
            self.y = self.radius
        
        return False
    
    
    def move(self):
        self.x += self.v_x
        self.y += self.v_y


class Paddle:
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
    
    return 0