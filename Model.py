# To process data for the logistic regression model, allowing a lightweight approach to be run on an Arduino

import math
import numpy as np

class_size = 10
d_x = 0.1
d_p = 0.1

def parse_data():

    file = open('readings.txt', 'r')
    lines = file.readlines()

    list = []

    for line in lines:
        sections = line.split(" ,")
        list.append([float(sections[1]), (sections[0] == "True")])

    sorted_list = sorted(list, key=lambda l:l[0])

    return sorted_list

def get_probabilities(input_list):
    classes = []

    number_of_classes = int(float(len(input_list))/float(class_size)) + 1

    for i in range(0, number_of_classes):
        if ((i * class_size) + class_size) <= len(input_list):
            classes.append(input_list[(i * class_size):((i * class_size) + class_size)])
        else:
            classes.append(input_list[(i * class_size):-1])
            break

    probabilities = []
    midpoints = []

    for group in classes:

        totalTrue = 0
        totalFalse = 0

        for element in group:
            if element[1]:
                totalTrue += 1
            else:
                totalFalse += 1

        probability = float(totalTrue)/float(totalFalse + totalTrue + d_p)

        probabilities.append(probability)

        # if class_size % 2 == 1:
        #     index = (class_size - 1)/2

        #     midpoints.append(group[index])
        # else:
        #     indexOne = int((len(group))/2) - 1
        #     indexTwo = 0
            
        #     if len(group) > 1:
        #         indexTwo = int((len(group))/2)

            # element1 = group[indexOne]
            # element2 = group[indexTwo]

            # mean = float(element1[0] + element2[0])/2.0

        midpoints.append(group[0][0]) # instead of mean, was originally indented

    return [midpoints, probabilities] # x, y format
    
def prep_for_linear_regression(input_lists):
    midpoints = input_lists[0]
    probabilities = input_lists[1]
    graphables = []

    for probability in probabilities:
        prob_ratio = float(probability) / (1.00 + d_x - float(probability)) + d_x
        graphables.append(float(math.log(prob_ratio)))

    return [midpoints, graphables]

def linear_regression(input_lists):
    # y = ax + b

    x = np.array(input_lists[0])
    y = np.array(input_lists[1])
    n = len(input_lists[0])

    m_x = float(np.mean(x))
    
    m_y = float(np.mean(y))

    SS_xy = float(np.sum(x * y)) - (n * m_x * m_y)
    SS_xx = float(np.sum(x * x)) - (n * m_x * m_x)

    a = SS_xy/SS_xx
    b = m_y - (m_x * a)

    return [a, b]



arr = get_probabilities(parse_data())

arr_p = prep_for_linear_regression(arr)

model = linear_regression(arr_p)


print(model) # P(event) = ax + b
