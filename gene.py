from random import randint
from math import exp
import player

SELECTION = 1000

class Gene:

    # p = probability of 1
    def __init__(self, chromo=[], num_of_chromo = 0, length_of_chromo = 0):
        self.chromo = chromo # stores chromosomes in a list
        self.num_of_chromo = num_of_chromo
        self.length_of_chromo = length_of_chromo

    def makeRandomGene(self, p=0.5):
        
        bound = round(p*SELECTION)

        for num in range(self.num_of_chromo):
            current_chromo = ''
            
            for l in range(self.length_of_chromo):
                x = randint(0, SELECTION)
                if x < bound:
                    current_chromo += '1'
                else:
                    current_chromo += '0'
            
            self.add(current_chromo)

    def add(self, chromosome):
        self.chromo.append(chromosome)

    def getChromo(self):
        return self.chromo

    def mutate(self, rate=0.1):
        bound = rate * SELECTION
        for i in range(self.num_of_chromo):
            for j in range(self.length_of_chromo):
                x = randint(0, SELECTION)

                if x < bound:
                    if self.chromo[i][j] == '1':
                        self.chromo[i][j] == '0'
                    else:
                        self.chromo[i][j] == '1'

    def crossover(self, gene):
        # assuming same number of chromosomes, crossover only once (not randomly)
        
        r = randint(1,self.num_of_chromo)
        chromo1 = self.chromo[0:r] + gene.getChromo()[r:]
        chromo2 = gene.getChromo()[0:r] + self.chromo[r:]

        gene1 = Gene(chromo1, self.num_of_chromo, self.length_of_chromo)
        gene2 = Gene(chromo2, self.num_of_chromo, self.length_of_chromo)

        gene1.mutate()
        gene2.mutate()

        return gene1, gene2


    