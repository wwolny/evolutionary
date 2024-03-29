import math
import random
import csv

class Individual():
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
        child = Individual()
        child.a = Individual.getRandomSet(self.a, partner.a).copy()
        child.b = Individual.getRandomSet(self.b, partner.b).copy()

        intersection = child.a.intersection(child.b)
        while len(intersection)>0:
            card = intersection.pop()
            Individual.getRandomSet(child.a, child.b).discard(card)
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
    def __init__(self, miSize, lambdaSize, A, B):
        self.miSize = miSize
        self.lambdaSize = lambdaSize
        self.A, self.B = A, B
        self.population = [Individual() for i in range(miSize)]
        self.children = []
        self.sort()

    def loss(self):
        loss = 0
        for individual in self.population:
            loss += individual.loss(self.A, self.B)
        return loss

    def sort(self):
        self.population.sort(key=lambda x: x.loss(self.A, self.B), reverse=False)

    def crossover(self):
        self.children=[]
        for i in range (self.lambdaSize):
            self.children.append(random.choice(list(self.population)))
        for index, individual in enumerate(self.children[:-1]):
            self.population.append(individual.crossover(self.children[index+1]))
        self.population.append(self.population[0].crossover(self.children[self.lambdaSize-1]))

    def mutation(self):
        for individual in self.population[self.miSize:]:
            individual.mutate()

    def selection(self):
        self.sort()
        self.population = self.population[:self.miSize]

    def lossTop(self):
        return self.population[0].loss(self.A, self.B)


def runTest():
    repeat = 1000
    AB = [[15,30], [1,20], [1,2], [13,11], [9,37], [50,10], [0,12]]
    epochs = 50
    resultsEnv = [0]*len(AB)
    resultsBestId = [0]*len(AB)
    resultsBestLoss = [0]*len(AB)
    for k in range(repeat):
        for j in range(len(AB)):
            env = Environment(miSize=10, lambdaSize=15, A=AB[j][0], B=AB[j][1])
            finished =False
            for i in range (epochs):
                env.crossover()
                env.mutation()
                env.selection()
                if env.lossTop() == 0.0:
                    resultsEnv[j] += env.loss()
                    resultsBestId[j] += i
                    resultsBestLoss[j] += env.lossTop()
                    finished =True
                    break;
            if not finished:
                resultsEnv[j] += env.loss()
                resultsBestId[j] += epochs-1
                resultsBestLoss[j] += env.lossTop()
    with open('miPlusLambdaTest.csv', mode='w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['envLoss', 'Iteration', 'bestFitLoss', 'AB'])
        for i in range(len(AB)):
            writer.writerow([resultsEnv[i]/repeat, resultsBestId[i]/repeat, resultsBestLoss[i]/repeat, AB[i]])

def simpleTest():
    epochs = 50
    resultsEnv = []
    resultsBest = []
    resultsBestLoss = []
    env = Environment(miSize=10, lambdaSize=15, A=5, B=50)
    for i in range (0, epochs):
        resultsEnv.append(env.loss())
        resultsBest.append(env.population[0])
        resultsBestLoss.append(env.lossTop())
        env.crossover()
        env.mutation()
        env.selection()

    with open('miPlusLambda.csv', mode='w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['envLoss', 'bestFit', 'bestFitLoss'])
        for i in range(epochs):
            writer.writerow([resultsEnv[i], resultsBest[i], resultsBestLoss[i]])


if __name__ == '__main__':
    runTest()
    simpleTest()
