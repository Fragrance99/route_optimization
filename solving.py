from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from classes.careworker import Careworker
from classes.residence import Residence


def print_solution(manager, routing, solution):
    print(f"Objective: {solution.ObjectiveValue()} minutes")
    index = routing.Start(0)
    plan_output = "Route for careworker 0:\n"
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += f" {manager.IndexToNode(index)} ->"
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(
            previous_index, index, 0)
    plan_output += f" {manager.IndexToNode(index)}\n"
    print(plan_output)
    plan_output += f"Route distance {route_distance} minutes\n"


def optimize_route(residences: list[Residence], careworkers: list[Careworker]):

    manager = pywrapcp.RoutingIndexManager(
        len(residences), 1, 0
    )

    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return residences[from_node].get_distance(residences[to_node])

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        print_solution(manager, routing, solution)

    # for start in residences:
    #     for dest in residences:
    #         print(f"{start.name} -> {dest.name}: {start.get_distance(dest)}")
