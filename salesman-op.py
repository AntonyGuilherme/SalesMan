
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from pso.util import read_cities, City
from typing import List, Tuple
import numpy
import matplotlib.pyplot as plt


def create_data_model(cities: List[City]):
    """Stores the data for the problem."""
    data = {}
    
    data["distance_matrix"] = numpy.zeros((len(cities), len(cities)), dtype=float)
    print(range(len(cities)))
    for from_city in range(len(cities)):
        for to_city in range(len(cities)):
            data["distance_matrix"][from_city,to_city] = cities[from_city].distance(cities[to_city])
            
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data


def print_solution(manager, routing, solution) -> List[Tuple[int,int]]:
    routes: List[Tuple[int,int]] = []
    
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()} miles")
    index = routing.Start(0)

    plan_output = "Route for vehicle 0:\n"
    route_distance = 0
    while not routing.IsEnd(index):
        city_from: int = manager.IndexToNode(index)
        plan_output += f" {manager.IndexToNode(index)} ->"
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        routes.append((city_from, manager.IndexToNode(index)))
    plan_output += f" {manager.IndexToNode(index)}\n"
    return routes


def create_route(manager, routing, solution) -> List[Tuple[int,int]]:
    routes: List[Tuple[int,int]] = []
    
    index = routing.Start(0)
    
    city_from = routing.Start(0)

    while not routing.IsEnd(index):
        city_from: int = manager.IndexToNode(index)
        
        index = solution.Value(routing.NextVar(index))
        
        city_to = solution.Value(routing.NextVar(city_from))
        
        routes.append((city_from, city_to))
    
    return routes

import time

def main():

    historic = []

    for exec in range(1, 50):
        tempo_inicio = time.time()
        """Entry point of the program."""
        cities: List[City] = read_cities()
        # Instantiate the data problem.
        data = create_data_model(cities)

        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(
            len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
        )

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data["distance_matrix"][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_parameters.solution_limit = 10000
        
        solution = routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        # if solution:
        #     routes = print_solution(manager, routing, solution)

            
        
        tempo_fim = time.time()
        tempo = tempo_fim - tempo_inicio
        historic.append(tempo)
        
        print(f"{exec} {tempo} {solution.ObjectiveValue()}")
    
    
    plt.title("Branch and Bound")
    plt.ylabel("Tempo Até Atingir os 761 metros (s)")
    plt.xlabel("Execuções")
    plt.plot(historic)
    plt.show()
        

main()