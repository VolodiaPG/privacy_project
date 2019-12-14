import numpy as np
import matplotlib.pyplot as plt
import LaunchMe
import csv


if __name__ == "__main__":

    with open('number_of_perturbationsSum.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Number of Pertubations", "Truth", "Average"])

        for jj in range(2, 7):
            # LaunchMe(sizeSet, maxValue, privacyParameter)
            launchMe = LaunchMe.LaunchMe(pow(10, 3), 1000, pow(10, -2), True)

            trueSum = launchMe.sum()
            print("[10^{}] True sum : {}".format(
                jj, trueSum))

            n = pow(10, jj)
            total = 0
            LaunchMe.printProgressBar(
                0, n, prefix='Progress:', suffix='Complete', length=50)
            for ii in range(0, n):
                sum = launchMe.sumPerturbated()
                # print("Count superior to {} perturbated: {}".format(sup, count))
                total += sum

                # Update Progress Bar
                LaunchMe.printProgressBar(
                    ii + 1, n, prefix='Progress:', suffix='Complete', length=50)

            average = total/n
            print("[10^{}] Average: {}".format(jj, average))
            writer.writerow(["10e{}".format(jj), trueSum,  average])
