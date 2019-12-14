from types import *
import numpy as np
import matplotlib.pyplot as plt
import Laplace


class LaunchMe():

    def __init__(self, sizeSet, maxValue, privacyParameter, testEnabled):
        super().__init__()

        self.testMode = testEnabled

        self.sizeSet = sizeSet
        self.maxValue = maxValue
        self.minValue = 0
        self.privacyParameter = privacyParameter
        self.set = np.random.randint(
            self.minValue,
            self.maxValue,
            self.sizeSet)

        self.laplace = Laplace.Laplace(self.privacyParameter)

        self.numberRequests = 0

    # reset the number of requests made to 0, and the budget consumed
    def zeroNumberRequest(self):
        self.numberRequests = 0

    # returns the cost of a request, incrementing the number of request by the numReqs
    def getFractionCost(self, numReqs):
        self.numberRequests += numReqs
        return pow(1/2, self.numberRequests)

    # COUNT not perturbated: SELECT COUNT(*) FROM set WHERE value > sup

    def count(self, sup):
        count = 0
        for i in self.set:
            if(i > sup):
                count += 1
        return count

    # COUNT but perturbated
    def countPerturbated(self, sup):
        if (self.testMode):
            self.laplace.enableTest()
        count = self.count(sup)

        # cost of a request set to 1
        cost = self.getFractionCost(1)
        count += self.laplace.genNoise(1, cost)

        if (self.testMode):
            self.laplace.disableTest()

        return count

    # SUM not perturbated : SELECT SUM(*) FROM set
    def sum(self):
        total = 0
        for i in self.set:
            total += i
        return total

    # SUM but perturbated
    def sumPerturbated(self):
        if (self.testMode):
            self.laplace.enableTest()

        total = self.sum()

        # cost of a request set to 1
        cost = self.getFractionCost(1)
        total += self.laplace.genNoise(self.maxValue, cost)

        if (self.testMode):
            self.laplace.disableTest()

        return total


# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        bar = ' ' * (length*len(fill) + len(prefix) +
                     len(suffix) + 5 + 2 + decimals + 3)
        print('\r%s' % (bar), end=printEnd)
        # print()


if __name__ == "__main__":
    # LaunchMe(sizeSet, maxValue, privacyParameter)
    launchMe = LaunchMe(pow(10, 3), 100, pow(10, -1), False)

    sup = 10
    print("True count superior to {}: {}".format(sup, launchMe.count(sup)))

    n = pow(10, 1)
    sum = 0
    # printProgressBar(0, n, prefix='Progress:', suffix='Complete', length=50)
    for ii in range(0, n):
        count = launchMe.countPerturbated(sup)
        print("Count superior to {} perturbated: {}".format(sup, count))
        sum += count

        # Update Progress Bar
        # printProgressBar(ii + 1, n, prefix='Progress:',
        #                  suffix='Complete', length=50)

    average = sum/n

    print("Average: {}".format(average))
