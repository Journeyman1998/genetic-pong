# Handles the control of the simulation

from player import Player, Population
import pygame, sys
import random, entity

NUM_OF_CHROMO = 5
LENGTH_OF_CHROMO = 10

WIDTH = 800
HEIGHT = 600


class Controller:

    def __init__(self, population_size, max_iter,decay):
        self.max_iter = max_iter
        self.population_size = population_size
        self.decay = decay
        self.iter_pop = [] # list of Population
        self.iter_score = []

        # initialise pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()

    def train(self):
        pop = Population()
        pop.makeNewPopulation(None, self.population_size, NUM_OF_CHROMO, LENGTH_OF_CHROMO)

        for iter_count in range(self.max_iter):
            pop.playGame(self.screen, self.clock)
            print(iter_count+1, ': ', pop.score())
            self.iter_pop.append(pop)
            self.iter_score.append(pop.score())

            new_genes = pop.sex()
            pop = Population()
            pop.makeNewPopulation(new_genes, self.population_size)
            self.population_size -= self.decay
    
    def printTrainStats(self):
        for i in range(len(self.iter_pop)):
            print(i, self.iter_score[i], sep=',', file=open('score.txt', 'w'))
            print(i, self.iter_score[i])
