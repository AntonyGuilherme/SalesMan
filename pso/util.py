import math
import random
import matplotlib.pyplot as plt
from numpy import zeros


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        return math.hypot(self.x - city.x, self.y - city.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"


def matrix_of_distances():
    
    cities = read_cities()
    
    distance_between_cities = zeros((len(cities), len(cities)), dtype=float)
    
    for from_city in range(len(cities)):
        for to_city in range(len(cities)):
            distance_between_cities[from_city,to_city] = cities[from_city].distance(cities[to_city])

def read_cities():
    cities = []
    with open('./data/cities.data', 'r') as handle:
        lines = handle.readlines()
        for line in lines:
            x, y = map(float, line.split())
            cities.append(City(x, y))
    return cities


def path_cost(route):
    return sum([city.distance(route[index - 1]) for index, city in enumerate(route)])


def visualize_tsp(title, cities):
    fig = plt.figure()
    fig.suptitle(title)
    x_list, y_list = [], []
    for city in cities:
        x_list.append(city.x)
        y_list.append(city.y)
    x_list.append(cities[0].x)
    y_list.append(cities[0].y)

    plt.plot(x_list, y_list, 'ro')
    #plt.plot(x_list, y_list, 'g')
    plt.show(block=True)