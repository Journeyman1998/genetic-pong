import math
from gene import Gene
import game

SCALE = 1000

def complementBinary(binary):
    answer = ''
    answer = answer.join('1' if x == '0' else '0' for x in binary[1:])
    answer = '0b0' + answer
    return answer

def convertToDecimal(chromosome):
    length = len(chromosome)
    positive = False
    if chromosome[0] == '1':
        positive = True
    
    if not positive:
        x = complementBinary(chromosome)
        return -(int(x, 2) + 1)
    else:
        x = '0b' + chromosome
        return int(x, 2)

class Player:
    def __init__(self, gene):
        self.weight = []
        self.gene = gene
        chromo = gene.getChromo()

        for i in range(len(chromo)):
            self.weight.append(convertToDecimal(chromo[i])/SCALE)
    
    def score(self, score):
        self.points = score
    
    def activation(self, z):
        return 1/(1 + math.exp(-z))
    
    def analyse(self, data):
        ball_x = data['ball_x']
        ball_y = data['ball_y']
        ball_v_x = data['ball_v_x']
        ball_v_y = data['ball_v_y']
        pad_y = data['pad_y']

        param = [ball_x, ball_y, ball_v_x, ball_v_y, pad_y]

        size = min(len(param), len(self.weight))

        i = total = 0
        for i in range(size):
            total += (self.weight[i] * param[i])
        
        
        # if total < pad_y:
        #     return 0
        # else:
        #     return 1

        total = self.activation(total)
        if total >= 0.4 and total <= 0.6:
            return 2
        else:
            return round(total)
    
    def getScore(self):
        return self.points

    def mate(self, player):
        return self.gene.crossover(player.gene)


class Population:
    def __init__(self):
        self.player = [] #list of Genes
        self.num_of_player = 0

    def addPlayer(self, player):
        self.player.append(player)
        self.num_of_player += 1

    def makeNewPopulation(self, list_of_genes=None, population_size=None, num_of_chromo=None, length_of_chromo=None):
        if list_of_genes == None:
            for i in range(population_size):
                gene = Gene([], num_of_chromo, length_of_chromo)
                gene.makeRandomGene()

                player = Player(gene)
                self.addPlayer(player)
        else:
            for i in range(population_size):
                player = Player(list_of_genes[i])
                self.addPlayer(player)

    def playGame(self, screen, clock):
        for i in range(self.num_of_player):
            game.startGame(self.player[i], screen, clock)

    def score(self):
        total = 0
        for p in self.player:
            total += p.getScore()
        return total

    def sex(self):
        self.player.sort(key=Player.getScore)
        list_of_genes = []

        for i in range(0, self.num_of_player, 2):
            gene1, gene2 = self.player[i].mate(self.player[i+1])
            list_of_genes.append(self.player[i].gene)
            list_of_genes.append(self.player[i+1].gene)
            list_of_genes.append(self.player[i].gene)
            list_of_genes.append(self.player[i+1].gene)
            list_of_genes.append(gene1)
            list_of_genes.append(gene2)
            

        return list_of_genes


