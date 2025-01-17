import enum
from ortools.constraint_solver import routing_enums_pb2, pywrapcp, routing_parameters_pb2
from classes.time_slot import minutes_to_time
from classes.careworker import Careworker
from classes.residence import Residence

# TODO  drop nodes if solution unfeasable
#       (penalty for using a vehicle -> maxing out shifts while still using as less careworkers as possible)


def print_solution(manager: pywrapcp.RoutingIndexManager, routing: pywrapcp.RoutingModel, solution: pywrapcp.Assignment, residences: list[Residence], careworkers: list[Careworker], dim_name: str):
    transit_time_dimension: pywrapcp.RoutingDimension = routing.GetDimensionOrDie(
        dim_name)
    total_time = 0  # of all careworkers

    dropped_residences = "Dropped Residences: "
    for node in range(routing.Size()):
        if routing.IsStart(node) or routing.IsEnd(node):
            continue
        if solution.Value(routing.NextVar(node)) == node:
            dropped_residences += f" {
                residences[manager.IndexToNode(node)].name}"
    print(dropped_residences)

    for cw_idx, cw in enumerate(careworkers):
        route_time = 0  # of current route
        residence_index = routing.Start(cw_idx)
        plan_output = f"Route for {cw.name}:\n"
        start_time = solution.Min(
            transit_time_dimension.CumulVar(residence_index))

        while not routing.IsEnd(residence_index):
            time_var = transit_time_dimension.CumulVar(residence_index)
            plan_output += (
                f"{residences[manager.IndexToNode(residence_index)].name}"
                f" Time({minutes_to_time(solution.Min(time_var)).isoformat()}, {minutes_to_time(solution.Max(
                    time_var) + residences[manager.IndexToNode(residence_index)].minutes_of_time_expense).isoformat()})"
                " -> "
            )
            residence_index = solution.Value(routing.NextVar(residence_index))

        time_var = transit_time_dimension.CumulVar(residence_index)
        end_time = solution.Min(time_var)
        route_time = end_time - start_time
        plan_output += (
            f"{residences[manager.IndexToNode(residence_index)].name}"
            f" Time({minutes_to_time(solution.Min(time_var)).isoformat()}, {minutes_to_time(solution.Max(
                time_var) + residences[manager.IndexToNode(residence_index)].minutes_of_time_expense).isoformat()})\n"
        )
        plan_output += f"Time of the route: {route_time} min\n"
        print(plan_output)
        total_time += route_time
    print(f"Total time of all routes: {total_time} min")


def optimize_route(residences: list[Residence], careworkers: list[Careworker]):

    time_dimension_name = "Transit Time"
    work_time_dimension_name = "Work Time"
    drop_residence_visits_penalty = 1000000
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
    def service_travel_time_callback(from_index: int, to_index: int) -> int:
        from_node_index: int = manager.IndexToNode(from_index)
        to_node_index: int = manager.IndexToNode(to_index)
        return residences[from_node_index].minutes_of_time_expense + residences[from_node_index].get_distance(residences[to_node_index])

    service_travel_time_callback_index = routing.RegisterTransitCallback(
        service_travel_time_callback)
    # define cost of each arc
    routing.SetArcCostEvaluatorOfAllVehicles(
        service_travel_time_callback_index)

    # create dimension to accumulate the distance of all careworkers in order for the solver to
    # be able to minimize the longest route and balance each route
    routing.AddDimension(
        evaluator_index=service_travel_time_callback_index,
        slack_max=1*60,  #
        capacity=24*60,  # 1 day -> can work from 0 hours to 24 hours a day
        fix_start_cumul_to_zero=False,
        name=time_dimension_name
    )
    transit_time_dimension: pywrapcp.RoutingDimension = routing.GetDimensionOrDie(
        time_dimension_name)
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

        # for the upper bound of time slots, service time would not be considered otherwise
        # i.e. 12:00-13:00 time slot -> careworker can still come at 13:00
        # -> edit time slots: upper bound - service time
        for interval in intervals:
            interval[1] = interval[1] - res.minutes_of_time_expense

        transit_time_dimension.CumulVar(index).SetRange(
            intervals[0][0], intervals[-1][1])
        for i in range(len(intervals)-1):
            transit_time_dimension.CumulVar(index).RemoveInterval(
                intervals[i][1], intervals[i+1][0])

    # instantiate route start and end times
    for cw_idx, cw in enumerate(careworkers):
        routing.AddVariableMinimizedByFinalizer(
            transit_time_dimension.CumulVar(routing.Start(cw_idx))
        )
        routing.AddVariableMinimizedByFinalizer(
            transit_time_dimension.CumulVar(routing.End(cw_idx)))

    # Work Time constraint -> balances work time and sets max work time
    routing.AddDimension(
        evaluator_index=service_travel_time_callback_index,
        slack_max=1*60,
        capacity=9*60,  # 9 hours -> can work 9 hours a day (including slack)
        fix_start_cumul_to_zero=False,
        name=work_time_dimension_name
    )
    work_time_dimension: pywrapcp.RoutingDimension = routing.GetDimensionOrDie(
        work_time_dimension_name)
    # penalty for not distributing work evenly
    work_time_dimension.SetGlobalSpanCostCoefficient(100)
    # penalty for long working times of vehicles
    work_time_dimension.SetSpanCostCoefficientForAllVehicles(10)

    # drop visits to residences if no solution found
    # do make starting depot removable
    for res_idx, res in enumerate(residences):
        if (res_idx > 0):
            routing.AddDisjunction([manager.NodeToIndex(
                res_idx)], drop_residence_visits_penalty)

    # solution heuristic
    search_parameters: routing_parameters_pb2.RoutingSearchParameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_MOST_CONSTRAINED_ARC
    )

    # solve
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        print_solution(manager=manager, routing=routing, solution=solution,
                       careworkers=careworkers, residences=residences, dim_name=time_dimension_name)
    else:
        print("No solution")
