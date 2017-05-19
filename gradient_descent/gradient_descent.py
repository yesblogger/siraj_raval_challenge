"""
Created: 17/05/2017
Author: Amartya Gupta
"""
from numpy import genfromtxt
import sys


def partial_dev(m, b, points, step):
    n = float(len(points))  # total number of data points in the data set
    m_grad = 0  # partial derivative of function cost with respect to m
    b_grad = 0  # partial derivative of function cost with respect to b
    for i in points:
        m_grad += -(2 / n) * i[0] * (i[1] - (m * i[0] + b))
        b_grad += -(2 / n) * (i[1] - (m * i[0] + b))
    m_new = m - step * m_grad  # adjusting the m value with respect to slop
    b_new = b - step * b_grad  # adjusting the b value with respect to slop
    step -= 0.000000001 * (m_grad + b_grad)  # dynamically adjusting the step
    # based on the slop of the gradient; the step increases with a steep
    # descent for faster convergence
    return (m_new, b_new, step)


def cost_function(m, b, points):
    # calculating the mean squared error; the data points are of type array
    SS = sum([(i[1] - (m * i[0] + b))**2 for i in points])
    return SS / float(len(points))


def gradient_descent(points):
    step = 0.000378  # it's the number by which the m_slop and b_int parameters
    # will be increased
    m_slop, b_int = ([0], [0])  # initiating the variables as list
    cost = [cost_function(m_slop[0], b_int[0], points)]
    # iterate as long as the recent cost output is the minimum in cost list
    while cost[0] == min(cost):
        m_temp, b_temp, step = partial_dev(m_slop[0], b_int[0], points, step)
        # inserting the new variables at index 0 for comparison with
        # previous minimum cost function output
        m_slop.insert(0, m_temp)
        b_int.insert(0, b_temp)
        cost.insert(0, cost_function(m_slop[0], b_int[0], points))
        # keep the size of m_slop, b_int and cost under 3 to manage memory
        if len(cost) > 3:
            m_slop.pop(3)
            b_int.pop(3)
            cost.pop(3)
        # printing the average squared sum of error on the screen
        print(cost[0])
    if len(cost) != 1:
        return (m_slop[1], b_int[1], cost[1])
    else:
        return (m_slop[0], b_int[0], cost[0])


def main(name):
    # importing the csv file as an numpy array
    points = genfromtxt(name, delimiter=',')
    # initiating the gradient descent algorithm
    m_slop, b_int, MSE = gradient_descent(points)
    print("Process complete!!!!")
    print()
    print("The best fit line has a slop of {} and y intercept of {}."
          .format(m_slop, b_int))
    print("After optimization we have gotten a mean squared error of {}."
          .format(MSE))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])  # calling the main function with command line input
    else:
        filename = input("Enter the name of the file: ")  # input for filename
        main(filename)
