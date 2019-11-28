import random
import math
import csv

class OnePlusOne():
    def __init__(self):
        while True:
            aLen = random.randint(0, 10)
            bLen = random.randint(0, 10)
            if aLen + bLen <= 10:
                break
        cardsRemaining = [True]*10
        self.a = [False]*10
        self.b = [False]*10
        cardsRemainingLen = 10
        for i in range (0, aLen):
            card = random.randint(0, cardsRemainingLen)
            for j in range(0, len(cardsRemaining)):
                if cardsRemaining[j] is True and card is 0:
                    cardsRemaining[j] = False
                    self.a[j] = True
                    break
                card -=1
            cardsRemainingLen -=1
        for i in range (0, bLen):
            card = random.randint(0, cardsRemainingLen)
            for j in range(0, len(cardsRemaining)):
                if cardsRemaining[j] is True and card is 0:
                    cardsRemaining[j] = False
                    self.b[j] = True
                    break
                card -=1
            cardsRemainingLen -=1

    @staticmethod
    def getRandomSet(set1, set2):
        if random.randint(0,1) == 0:
            return set1
        return set2

    def loss(self, A, B):
        sumA, sumB  = 0, 0
        for card in range(0, 10):
            if self.a[card] is True:
                sumA += (card+1)
            if self.b[card] is True:
                sumB += (card+1)
        return math.sqrt((A-sumA)**2 + (B-sumB)**2)

    def setAB(self, parent):
        for i in range(0,10):
            self.a[i] = parent.a[i]
            self.b[i] = parent.b[i]

    def mutate (self, sig):
        card = int(sig*random.lognormvariate(0,10))%10
        if self.a[card] is True:
            self.a[card] = False
            self.b[card] = True
        elif self.b[card] is True:
            self.b[card] = False
        else:
            self.a[card] = True


    def __str__(self):
        strA = "A: "
        strB = "B: "
        for i in range(0,10):
            if self.a[i] is True:
                strA += str(i+1)
                strA += ", "
            if self.b[i] is True:
                strB += str(i+1)
                strB += ", "
        return strA + '\n' +strB + '\n'



class EnvironmentOnePlusOne():
    def __init__(self, size, A, B):
        self.size = size
        self.A, self.B = A, B
        self.population = [OnePlusOne() for i in range(size)]
        self.m = 10
        self.c1 = 0.82
        self.c2 = 1.2
        self.sig = 5.0

    def loss(self):
        loss = 0
        for genotype in self.population:
            loss += genotype.loss(self.A, self.B)
        return loss

    def lossTop(self):
        return self.population[0].loss(self.A, self.B)

    def sort(self):
        self.population.sort(key=lambda x: x.loss(self.A, self.B), reverse=False)

    def mutation(self):
        y_ch = 0
        child = OnePlusOne()
        for i in range(int(self.size/self.m)):
            for j in range(i*self.m, self.size):
                child.setAB(self.population[j])
                child.mutate(self.sig)
                if self.population[j].loss(self.A, self.B) > child.loss(self.A, self.B):
                    self.population[j].setAB(child)
                    y_ch += 1
            fi = y_ch/self.m
            if fi > 0.2:
                self.sig *= self.c2
            elif fi <0.2:
                self.sig *= self.c1


def runTest():
    repeat = 1000
    AB = [[15,30], [1,20], [1,2], [13,11], [9,37], [50,10], [0,12]]
    epochs = 50
    resultsEnv = [0]*len(AB)
    resultsBestId = [0]*len(AB)
    resultsBestLoss = [0]*len(AB)
    for k in range(repeat):
        for j in range(len(AB)):
            env = EnvironmentOnePlusOne(15, AB[j][0], AB[j][1])
            env.sort()
            finished =False
            for i in range(epochs):
                env.mutation()
                env.sort()
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

    with open('onePlusOneTest.csv', mode='w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['envLoss', 'Iteration', 'bestFitLoss', 'AB'])
        for i in range(len(AB)):
            writer.writerow([resultsEnv[i]/repeat, resultsBestId[i]/repeat, resultsBestLoss[i]/repeat, AB[i]])

def simpleTest():
    epochs = 50
    resultsEnv = []
    resultsBest = []
    resultsBestLoss = []
    env = EnvironmentOnePlusOne(15, 5, 50)
    env.sort()
    for i in range (0, epochs):
        resultsEnv.append(env.loss())
        resultsBest.append(env.population[0])
        resultsBestLoss.append(env.lossTop())
        env.mutation()
        env.sort()

    with open('onePlusOne.csv', mode='w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['envLoss', 'bestFit', 'bestFitLoss'])
        for i in range(epochs):
            writer.writerow([resultsEnv[i], resultsBest[i], resultsBestLoss[i]])


if __name__ == '__main__':
    runTest()
    simpleTest()
