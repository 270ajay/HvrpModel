from ortools.constraint_solver import pywrapcp
import utilities, constraints, logging


def buildAndSolveOptimizationModel(data):

    logging.info("building Optimization Model")

    manager = pywrapcp.RoutingIndexManager(data['orderDetails']['numOfNodes'],
                                           data['vehicleDetails']['numOfVehicles'],
                                           data['vehicleDetails']['startDepotIndices'],
                                           data['vehicleDetails']['endDepotIndices'])
    routing = pywrapcp.RoutingModel(manager)


    demandCallBackIndex = utilities.getDemandFunction(manager, routing,  data)
    transitCallBackIndices = utilities.getTravelTimeFunctionsList(data, routing, manager)
    serviceCallBackIndices = utilities.getServiceTimeFunctionsList(data, routing, manager)


    constraints.minimizeTransit(data, routing, transitCallBackIndices)
    constraints.minimizeNumberOfVehicles(data, routing)
    timeDimension = constraints.createCtForWaitingAndMaxTime(data, routing, serviceCallBackIndices)
    constraints.createCtForStartTime(data, routing, timeDimension)
    constraints.createCtForTimeWindows(data, routing, manager, timeDimension)
    constraints.createCtForMaxWorkingHours(data, routing, timeDimension)
    constraints.createCtForCapacity(data, routing, demandCallBackIndex)
    constraints.addCostForNodes(data, routing, manager)


    searchParameters = pywrapcp.DefaultRoutingSearchParameters()
    searchParameters = constraints.updateSearchParameters(data, searchParameters)



    logging.info("optimizing...")
    assignment = routing.SolveWithParameters(searchParameters)
    logging.info("optimization done\n")

    if assignment:
        utilities.printOutputToCsv(data, manager, routing, assignment, timeDimension)