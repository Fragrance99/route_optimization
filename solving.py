from ortools.constraint_solver import routing_enums_pb2, pywrapcp, routing_parameters_pb2

from classes.careworker import Careworker
from classes.residence import Residence


def print_solution(manager: pywrapcp.RoutingIndexManager, routing: pywrapcp.RoutingModel, solution: pywrapcp.Assignment, residences: list[Residence], careworkers: list[Careworker]):
    transit_time_dimension = routing.GetDimensionOrDie("Transit Time")
    total_time = 0
    for cw_idx, cw in enumerate(careworkers):
        index = routing.Start(cw_idx)
        plan_output = f"Route for {cw.name}:\n"
        while not routing.IsEnd(index):
            time_var = transit_time_dimension.CumulVar(index)
            plan_output += (
                f"{residences[manager.IndexToNode(index)].name}"
                f" Time({solution.Min(time_var) - residences[manager.IndexToNode(
                    index)].minutes_of_time_expense}, {solution.Max(time_var)})"
                " -> "
            )
            index = solution.Value(routing.NextVar(index))

        time_var = transit_time_dimension.CumulVar(index)
        plan_output += (
            f"{residences[manager.IndexToNode(index)].name}"
            f" Time({solution.Min(time_var) - residences[manager.IndexToNode(
                index)].minutes_of_time_expense}, {solution.Max(time_var)})\n"
        )
        plan_output += f"Time of the route: {solution.Min(time_var)} min\n"
        print(plan_output)
        total_time += solution.Min(time_var)
    print(f"Total time of all routes: {total_time} min")


def optimize_route(residences: list[Residence], careworkers: list[Careworker]):

    depot_index = 0
    for res in residences:
        if res.id == 0:
            depot_index = 0

    # create routing index manager
    manager = pywrapcp.RoutingIndexManager(
        len(residences), len(careworkers), depot_index)
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
        slack_max=120,  #
        capacity=1440,  # 1 day
        fix_start_cumul_to_zero=False,
        name=transit_time_dimension_name
    )
    transit_time_dimension: pywrapcp.RoutingDimension = routing.GetDimensionOrDie(
        transit_time_dimension_name)
    # penalty for large difference between min route distance and max route distance
    transit_time_dimension.SetGlobalSpanCostCoefficient(100)
    # coefficient applied to travel costs such that the difference defined above gets even bigger
    transit_time_dimension.SetSpanCostCoefficientForAllVehicles(10)

    # add time windows constraints
    # first add min and max of all time windows
    # then remove the forbidden intervals from CumulVar
    for residence_idx, res in enumerate(residences):
        index: int = manager.NodeToIndex(residence_idx)

        # intervals are ordered
        intervals = res.get_time_slots_as_intervals()

        transit_time_dimension.CumulVar(index).SetRange(
            intervals[0][0], intervals[-1][1])
        for i in range(len(intervals)-1):
            transit_time_dimension.CumulVar(index).RemoveInterval(
                intervals[i][1], intervals[i+1][0])

    # instantiate route start and end times
    for cw_idx, cw in enumerate(careworkers):
        routing.AddVariableMaximizedByFinalizer(
            transit_time_dimension.CumulVar(routing.Start(cw_idx))
        )
        routing.AddVariableMinimizedByFinalizer(
            transit_time_dimension.CumulVar(routing.End(cw_idx)))

    # solution heuristic
    search_parameters: routing_parameters_pb2.RoutingSearchParameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_MOST_CONSTRAINED_ARC
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
