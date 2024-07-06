from ortools.constraint_solver import routing_enums_pb2, pywrapcp, routing_parameters_pb2

from classes.careworker import Careworker
from classes.residence import Residence


def print_solution(manager: pywrapcp.RoutingIndexManager, routing: pywrapcp.RoutingModel, solution: pywrapcp.Assignment, residences: list[Residence], careworkers: list[Careworker]):
    print(f"Objective: {solution.ObjectiveValue()}")
    max_route_distance = 0
    for cw_index, cw in enumerate(careworkers):
        index = routing.Start(cw_index)

        plan_output = f"Route for careworker {cw.name}:\n"

        route_distance = 0

        while not routing.IsEnd(index):
            plan_output += f"{
                residences[manager.IndexToNode(index)].name} -> "

            previous_index = index

            index = solution.Value(routing.NextVar(index))

            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, cw_index)

        plan_output += f"{residences[manager.IndexToNode(index)].name}\n"

        plan_output += f"Distance of the route: {route_distance} min\n"

        print(plan_output)

        max_route_distance = max(route_distance, max_route_distance)

    print(f"Maximum of the route distances: {max_route_distance} min")


def optimize_route(residences: list[Residence], careworkers: list[Careworker]):

    # create routing index manager
    manager = pywrapcp.RoutingIndexManager(
        len(residences), len(careworkers), 0)
    # create routing model
    routing = pywrapcp.RoutingModel(manager)

    # TRANSIT TIME DIMENSION
    # consists of travel time + service time at the destination node
    # create and register transit callback
    def transit_time_callback(from_index: int, to_index: int) -> int:
        from_node: int = manager.IndexToNode(from_index)
        to_node: int = manager.IndexToNode(to_index)
        return residences[from_node].get_distance(residences[to_node]) + residences[to_node].minutes_of_time_expense

    transit_callback_index = routing.RegisterTransitCallback(
        transit_time_callback)
    # define cost of each arc
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # create dimension to accumulate the distance of all careworkers in order for the solver to
    # be able to minimize the longest route and balance each route
    transit_time_dimension_name = "Transit Time"
    routing.AddDimension(
        evaluator_index=transit_callback_index,
        slack_max=0,
        capacity=600,
        fix_start_cumul_to_zero=True,
        name=transit_time_dimension_name
    )
    transit_time_dimension: pywrapcp.RoutingDimension = routing.GetDimensionOrDie(
        transit_time_dimension_name)
    # penalty for large difference between min route distance and max route distance
    transit_time_dimension.SetGlobalSpanCostCoefficient(100)
    # coefficient applied to travel costs such that the difference defined above gets even bigger
    transit_time_dimension.SetSpanCostCoefficientForAllVehicles(10)

    # solution heuristic
    search_parameters: routing_parameters_pb2.RoutingSearchParameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # solve
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        print_solution(manager=manager, routing=routing, solution=solution,
                       careworkers=careworkers, residences=residences)
    else:
        print("No solution")

    # for start in residences:
    #     for dest in residences:
    #         print(f"{start.name} -> {dest.name}: {start.get_distance(dest)}")
