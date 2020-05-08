
from controller import Controller

if __name__ == '__main__':
    god = Controller(population_size=50, max_iter=20, decay=0)
    god.train()
    god.printTrainStats()