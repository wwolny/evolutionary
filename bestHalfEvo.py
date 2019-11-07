import copy
import math
import random
import csv

class Genotype():
    def __init__(self):
        while True:
            aLen = random.randint(0, 10)
            bLen = random.randint(0, 10)
            if aLen + bLen <= 10:
                break
        cardsRemaining = {i for i in range (1, 11)}
        self.a = set()
        self.b = set()
        for i in range (0, aLen):
            card = random.choice(list(cardsRemaining))
            cardsRemaining.discard(card)
            self.a.add(card)
        for i in range (0, bLen):
            card = random.choice(list(cardsRemaining))
            cardsRemaining.discard(card)
            self.b.add(card)

    @staticmethod
    def getRandomSet(set1, set2):
        if random.randint(0,1) == 0:
            return set1
        return set2

    def loss(self, A, B):
        sumA, sumB  = 0, 0
        for card in list(self.a):
            sumA += card
        for card in list(self.b):
            sumB += card
        return math.sqrt((A-sumA)**2 + (B-sumB)**2)

    def crossover(self, partner):
        child = Genotype()
        child.a = Genotype.getRandomSet(self.a, partner.a).copy()
        child.b = Genotype.getRandomSet(self.b, partner.b).copy()

        intersection = child.a.intersection(child.b)
        while len(intersection)>0:
            card = intersection.pop()
            Genotype.getRandomSet(child.a, child.b).discard(card)
        return child

    def mutate (self):
        card = random.randint(1, 10)
        if card in self.a or card in self.b:
                self.a.discard(card)
                self.b.discard(card)
                return
        mutSet = self.getRandomSet(self.a, self.b)
        mutSet.add(card)

    def __str__(self):
        return str(self.a) + '\n' +str(self.b) + '\n'


class Environment():
    def __init__(self, size, A, B):
        self.size = size
        self.A, self.B = A, B
        self.population = [Genotype() for i in range(size)]

    def loss(self):
        loss = 0
        for genotype in self.population:
            loss += genotype.loss(self.A, self.B)
        return loss

    def lossTop(self):
        return self.population[0].loss(self.A, self.B)

    def sort(self):
        self.population.sort(key=lambda x: x.loss(self.A, self.B), reverse=False)

    def selection(self):
        self.population = self.population[:self.size//2]

    def crossover(self):
        for index in range (self.size//2-1):
            genotype = self.population[index]
            self.population.append(genotype.crossover(self.population[index+1]))
        genotype = self.population[self.size//2-1]
        self.population.append(genotype.crossover(self.population[0]))

    def mutation(self):
        for genotype in self.population[self.size//2:]:
            genotype.mutate()
        self.sort()

    # def print(self):
    #     print("TOTAL GENERATION LOSS: " + str(self.loss()))
    #     for genotype in self.population:
    #         print("LOSS: " + str(genotype.loss(self.A, self.B)))
    #         print (genotype.a)
    #         print (genotype.b)
    #         print ("   ")

if __name__ == '__main__':
    epochs = 50
    resultsEnv = []
    resultsBest = []
    env = Environment(50, 15, 30)
    env.sort()
    for i in range (epochs):
        env.selection()
        env.crossover()
        env.mutation()
        print(env.loss())
        resultsEnv.append(env.loss())
        resultsBest.append(env.population[0])
    print(env.population[0])
    print(env.lossTop())
    with open('lambdaMi.csv', mode='w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['envLoss', 'bestFit'])
        for i in range(epochs):
            writer.writerow([resultsEnv[i], resultsBest[i]])
