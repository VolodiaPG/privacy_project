import random
import numpy as np
import csv
import matplotlib.pyplot as plt

class Laplace():
    """
    Laplace attributes:
    epsilon : the total epsilon we have
    epsilonConsumed : tells how much of the total epsilon is consumed (is between 0 and 1)
    testModeEnabled : tells us if the class is in test mode or not
    """

    def __init__(self, epsilon):
        self.epsilon = epsilon
        self.epsilonConsumed = 0
        self.testModeEnabled = False
        self.testCSVFile = "test.csv"

    def enableTest(self):
        self.testModeEnabled = True
    
    def disableTest(self):
        self.testModeEnabled = False

    def test(self, numberPertu, sensitivity):
        self.enableTest()

        count = [0] * 50
        generatedValue = [0] * numberPertu
        try:
            for i in range(0, numberPertu):
                # Generates a random noise from the sensitivity. 1 is an arbitrary number without any meaning,
                # and we don't use it because we are in test mode
                x = self.genNoise(sensitivity, 1)
                generatedValue[i] = x
                # Checks if we are in the interval [-500, 500]
                if(x >= -500 and x <= 500):
                    # Adds 500 (to be in the interval [0;1000])
                    temp = x + 500
                    # Divides by 20 to have the interval length of 20
                    index = temp/20
                    # Increments the count by 1
                    count[int(index)] += 1

        except(NotEnoughBudgetException):
            print("Not enough budget")
            pass

        with open(self.testCSVFile, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["Interval", "Occurences"])
            for ii in range(len(count)):
                # where a & b are the limits of the interval
                a = ii * 20 - 500
                b = ii * 20 - 480
                writer.writerow(["[{}, {}[".format(a, b), count[ii]])
        
        plt.hist(generatedValue, bins=50)
        plt.xlabel('Interval')
        plt.ylabel('Count')
        plt.show()

        self.disableTest()

    """
    Generates the noise for a given sensitivity and consumes a fraction the total epsilon
    """
    def genNoise(self, sensitivity, fraction):
        #tests if we are not in test mode and if we can't consume epsilon then raise an exception
        if(((self.epsilonConsumed > 1) or (self.epsilonConsumed + fraction > 1)) and (not self.testModeEnabled)):
            raise NotEnoughBudgetException("Not enough budget")
        
        # tests if test mode enabled then put fraction to 1 so taht we can use the rest normally
        if(self.testModeEnabled):
            fraction = 1
      #Generation of the noise:
        #Adds the fraction to epsilonConsumed
        self.epsilonConsumed += fraction
        #Generates a random number in [-1/2; 1/2]
        u = random.random() - 1/2
        #defines parameters
        mu = 0
        scalingFactor = sensitivity/(self.epsilon*fraction) # epsilon * fraction : it is for having a % of the epsilon total
        #Calculates the noise: source Wikipedia
        noise = mu - scalingFactor * np.sign(u)*np.log(1 - 2 * np.abs(u))
        return noise



"""
Just a random Exception class
"""
class NotEnoughBudgetException(Exception):
    pass

if __name__ == "__main__":
    laplace = Laplace(0.1)
    laplace.test(pow(10,4), 1)