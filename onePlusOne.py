##Wojciech Wolny OnePlusOne
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
            self.a[card] = True
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

if __name__ == '__main__':
    epochs = 50
    resultsEnv = []
    resultsBest = []
    env = EnvironmentOnePlusOne(50, 15, 30)
    env.sort()
    for i in range (epochs):
        env.mutation()
        resultsEnv.append(env.loss())
        resultsBest.append(env.population[0])
        env.sort()
        print(env.loss())

    print(env.population[0])
    print(env.lossTop())
    with open('onePlusOne.csv', mode='w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['envLoss', 'bestFit'])
        for i in range(epochs):
            writer.writerow([resultsEnv[i], resultsBest[i]])
