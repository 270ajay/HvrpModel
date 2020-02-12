from ortools.constraint_solver import pywrapcp
import utilities, constraints, logging


def buildAndSolveOptimizationModel(data):

    logging.info("building Optimization Model")

    routing = pywrapcp.RoutingModel(data['orderDetails']['numOfNodes'],
                                    data['vehicleDetails']['numOfVehicles'],
                                    data['vehicleDetails']['startDepotIndices'],
                                    data['vehicleDetails']['endDepotIndices'])


    demandCallBackIndex = utilities.getDemandFunction(data)
    transitCallBackIndices = utilities.getTravelTimeFunctionsList(data)
    serviceCallBackIndices = utilities.getServiceTimeFunctionsList(data)


    constraints.minimizeTransit(data, routing, transitCallBackIndices)
    constraints.minimizeNumberOfVehicles(data, routing)
    timeDimension = constraints.createCtForWaitingAndMaxTime(data, routing, serviceCallBackIndices)
    constraints.createCtForStartTime(data, routing, timeDimension)
    constraints.createCtForTimeWindows(data, routing, timeDimension)
    constraints.createCtForMaxWorkingHours(data, routing, timeDimension)
    constraints.createCtForCapacity(data, routing, demandCallBackIndex)
    constraints.addCostForNodes(data, routing)


    searchParameters = pywrapcp.RoutingModel.DefaultSearchParameters()
    searchParameters = constraints.updateSearchParameters(data, searchParameters)



    logging.info("optimizing...")
    assignment = routing.SolveWithParameters(searchParameters)
    logging.info("optimization done\n")

    if assignment:
        utilities.printOutputToCsv(data, routing, assignment, timeDimension)