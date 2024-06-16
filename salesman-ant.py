import pants
from pso.util import read_cities
from numpy import zeros
import matplotlib.pyplot as plt

cities = read_cities()

distance_between_cities = zeros((len(cities), len(cities)), dtype=float)
    
for from_city in range(len(cities)):
    for to_city in range(len(cities)):
        distance_between_cities[from_city,to_city] = cities[from_city].distance(cities[to_city])

def dist(cid1, cid2):
  return distance_between_cities[cid1][cid2]

nodes = list(range(len(cities)))

world = pants.World(nodes, dist)

solver = pants.Solver(limit=600, ant_count=30, beta=8)

historic = []
solution = solver.solve(world, historic)

print('Caminho:', solution.tour)
print('Custo Total:', solution.distance)

plt.title("Colônia de Formigas")
plt.xlabel("Número de Execuções")
plt.ylabel("Distâncias")
plt.plot(historic)
plt.show()

