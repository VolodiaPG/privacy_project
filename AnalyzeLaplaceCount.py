import numpy as np
import matplotlib.pyplot as plt
import LaunchMe
import csv


if __name__ == "__main__":

    with open('number_of_perturbations.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Number of Pertubations", "Truth", "Average"])

        for jj in range(2, 7):
            # LaunchMe(sizeSet, maxValue, privacyParameter)
            launchMe = LaunchMe.LaunchMe(pow(10, 3), 100, pow(10, -4), True)

            sup = 10
            trueCount = launchMe.count(sup)
            print("[10^{}] True count superior to {}: {}".format(
                jj, sup, trueCount))

            n = pow(10, jj)
            sum = 0
            LaunchMe.printProgressBar(
                0, n, prefix='Progress:', suffix='Complete', length=50)
            for ii in range(0, n):
                count = launchMe.countPerturbated(sup)
                # print("Count superior to {} perturbated: {}".format(sup, count))
                sum += count

                # Update Progress Bar
                LaunchMe.printProgressBar(
                    ii + 1, n, prefix='Progress:', suffix='Complete', length=50)

            average = sum/n
            print("[10^{}] Average: {}".format(jj, average))
            writer.writerow(["10e{}".format(jj), trueCount,  average])
