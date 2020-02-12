import utilities, logging
from ortools.constraint_solver import routing_enums_pb2



def minimizeTransit(data, routing, transitCallBackIndices):
    for vehicleId in range(data['vehicleDetails']['numOfVehicles']):
        routing.SetArcCostEvaluatorOfVehicle(transitCallBackIndices[vehicleId], vehicleId)
    logging.info("minimizing travel times")




def createCtForWaitingAndMaxTime(data, routing, serviceCallBackIndices):

    routing.AddDimensionWithVehicleTransitAndCapacity(
        serviceCallBackIndices,
        data['modelParams']['maxWaiting'],
        data['vehicleDetails']['maxEndTimeList'],
        False,
        utilities.TIME_DIMENSION)
    timeDimension = routing.GetDimensionOrDie(utilities.TIME_DIMENSION)
    logging.info("added waiting time and max time constraint")
    return timeDimension





def createCtForTimeWindows(data, routing, manager, timeDimension):

    for locationIndex in range(data['orderDetails']['numOfNodes']):
        index = manager.NodeToIndex(locationIndex)
        if (routing.IsStart(index)) or (routing.IsEnd(index)):
            continue
        timeDimension.CumulVar(index).SetRange(data['orderDetails']['minEntryTimeList'][locationIndex], data['orderDetails']['maxEntryTimeList'][locationIndex])

    logging.info("added time window constraints")





def createCtForStartTime(data, routing, timeDimension):

    for vehicleId in range(data['vehicleDetails']['numOfVehicles']):
        index = routing.Start(vehicleId)
        timeDimension.CumulVar(index).SetRange(data['vehicleDetails']['minStartTimeList'][vehicleId],
                                                data['vehicleDetails']['maxStartTimeList'][vehicleId])

    logging.info("added start time constraints")





def createCtForCapacity(data, routing, demandCallBackIndex):

    routing.AddDimensionWithVehicleCapacity(
        demandCallBackIndex,
        0,
        data['vehicleDetails']['capacityList'],
        True,
        utilities.CAPACITY_DIMENSION)

    logging.info("added capacity constraints")





def addCostForNodes(data, routing, manager):
    for node in range(data['orderDetails']['numOfNodes']):
        routing.AddDisjunction([manager.NodeToIndex(node)], data['orderDetails']['costOfNotServingList'][node])

    logging.info("added costs for not visiting nodes")




def minimizeNumberOfVehicles(data, routing):
    for i in range(data['vehicleDetails']['numOfVehicles']):
        routing.SetFixedCostOfVehicle(data['vehicleDetails']['costList'][i], i)

    logging.info("minimizing number of vehicles used")




def updateSearchParameters(data, searchParameters):
    searchParameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    searchParameters.time_limit.seconds = data['modelParams']['solverTimeLimit']
    searchParameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

    if data['modelParams']['displaySolverSearch']:
        searchParameters.log_search = True

    logging.info("updated search parameters for optimization")
    return searchParameters





def createCtForMaxWorkingHours(data, routing, timeDimension):

    for i in range(data['vehicleDetails']['numOfVehicles']):
        totalDurationExpression = timeDimension.CumulVar(routing.End(i)) - timeDimension.CumulVar(routing.Start(i))
        routing.solver().Add(totalDurationExpression <= data['vehicleDetails']['maxWorkingHoursList'][i])
        routing.AddVariableMaximizedByFinalizer(timeDimension.CumulVar(routing.Start(i)))
        routing.AddVariableMinimizedByFinalizer(timeDimension.CumulVar(routing.End(i)))

    logging.info("added max working hours constraints")




# def instantiateRouteStartAndEndTimes(data, routing, timeDimension):
#
#     for i in range(data['numVehicles']):
#         routing.AddVariableMinimizedByFinalizer(timeDimension.CumulVar(routing.Start(i)))
#         routing.AddVariableMinimizedByFinalizer(timeDimension.CumulVar(routing.End(i)))
#
#     logging.info("instantiated route start and end times")