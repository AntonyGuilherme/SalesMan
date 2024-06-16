from pso.util import City, read_cities, visualize_tsp
import matplotlib.pyplot as plt
from typing import List

title: str = "Caixeiro Viajante"
cities: List[City] = read_cities()

fig = plt.figure()
fig.suptitle(title)
x_list, y_list = [], []
for city in cities:
    x_list.append(city.x)
    y_list.append(city.y)
    x_list.append(cities[0].x)
    y_list.append(cities[0].y)

plt.plot(x_list, y_list, 'ro')
plt.show(block=True)