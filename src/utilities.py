import logging, csv
from datetime import timedelta

TIME_DIMENSION = "TIME_DIMENSION"
CAPACITY_DIMENSION = "CAPACITY_DIMENSION"



def getTravelTimeFunction(data, speedFactor):
    """Returns the travel time between the two nodes."""
    # Convert from routing variable Index to time matrix NodeIndex.

    def travelTimeCallback(fromNode, toNode):
        fromLoc = data['orderDetails']['locationList'][fromNode]
        toLoc = data['orderDetails']['locationList'][toNode]
        return round(data['timeMatrix'][fromLoc][toLoc]/speedFactor)

    return travelTimeCallback




def getServiceTimeFunction(data, speedFactor, serviceTimeFactor):
    """Returns the travel + service time between the two nodes."""
    # Convert from routing variable Index to time matrix NodeIndex.

    def serviceTimeCallback(fromNode, toNode):
        fromLoc = data['orderDetails']['locationList'][fromNode]
        toLoc = data['orderDetails']['locationList'][toNode]
        return round(data['timeMatrix'][fromLoc][toLoc]/speedFactor) + round(data['orderDetails']['serviceTime'][fromNode]/serviceTimeFactor)

    return serviceTimeCallback



def getDemandFunction(data):
    """Returns the demand of the node."""
    # Convert from routing variable Index to demands NodeIndex.

    def demandCallBack(fromNode, toNode):
        return data['orderDetails']['demandList'][fromNode]

    return demandCallBack





def getTravelTimeFunctionsList(data):

    transitCallBackIndices = []

    for vehicleId in range(data['vehicleDetails']['numOfVehicles']):
        speedFactor = data['vehicleDetails']['speedFactorList'][vehicleId]
        transitCallBackIndices.append(getTravelTimeFunction(data, speedFactor))

    return transitCallBackIndices




def getServiceTimeFunctionsList(data):

    serviceCallBackIndices = []

    for vehicleId in range(data['vehicleDetails']['numOfVehicles']):
        speedFactor = data['vehicleDetails']['speedFactorList'][vehicleId]
        serviceTimeFactor = data['vehicleDetails']['serviceTimeFactorList'][vehicleId]
        serviceCallBackIndices.append(getServiceTimeFunction(data, speedFactor, serviceTimeFactor))

    return serviceCallBackIndices




def getNumberOfVehiclesUsed(data, routing, assignment):

    numOfVehiclesUsed = 0
    for i in range(data["vehicleDetails"]["numOfVehicles"]):
        if routing.IsVehicleUsed(assignment, i):
            logging.info("Vehicle: " + str(data["vehicleDetails"]["vehicleNameList"][i]) + " is used")
            numOfVehiclesUsed += 1

    logging.info("Total number of vehicles used: "+str(numOfVehiclesUsed))
    return numOfVehiclesUsed




def printOutputToCsv(data, routing, assignment, timeDimension):

    numOfVehiclesUsed = getNumberOfVehiclesUsed(data, routing, assignment)
    with open("../output/OptimizerOutput.csv", "w", newline='') as file:
        dataWriter = csv.writer(file)
        dataWriter.writerow(['Optimizer Output', 'TotalVehiclesUsed:', str(numOfVehiclesUsed)])


        for vehicleId in range(data['vehicleDetails']['numOfVehicles']):
            if routing.IsVehicleUsed(assignment, vehicleId):

                dataWriter.writerow([""])
                dataWriter.writerow([""])
                dataWriter.writerow(['Vehicle', 'Order', 'Location', 'OriginalTravelTime', 'TravelTime', 'ArriveAt', 'ArriveAtLatest',
                                      'OriginalServiceTime', 'ServiceTime', 'LeaveAt', 'LeaveAtLatest', 'Demand', 'Capacity', 'PreviousLocation'])

                index = routing.Start(vehicleId)
                while not routing.IsEnd(index):

                    node_index = routing.IndexToNode(index)
                    next_node_index = routing.IndexToNode(assignment.Value(routing.NextVar(index)))
                    timeVar = timeDimension.CumulVar(assignment.Value(routing.NextVar(index)))
                    timeMin = assignment.Min(timeVar)
                    timeMax = assignment.Max(timeVar)

                    vehicleName = str(data['vehicleDetails']['vehicleNameList'][vehicleId])
                    orderId = str(data['orderDetails']['orderList'][next_node_index])
                    locationName = str(data['orderDetails']['locationList'][next_node_index])
                    originalServiceTime = data['orderDetails']['serviceTime'][next_node_index]
                    serviceTimeFactor = data['vehicleDetails']['serviceTimeFactorList'][vehicleId]
                    serviceTime = round(originalServiceTime / serviceTimeFactor)
                    demand = data['orderDetails']['demandList'][next_node_index]
                    capacity = data['vehicleDetails']['capacityList'][vehicleId]
                    previousLocationName = str(data['orderDetails']['locationList'][node_index])
                    originalTravelTime = data["timeMatrix"][previousLocationName][locationName]
                    speedFactor = data['vehicleDetails']['speedFactorList'][vehicleId]
                    travelTime = round(originalTravelTime / speedFactor)


                    dataWriter.writerow([vehicleName, orderId, locationName, originalTravelTime, travelTime,
                                         str(timedelta(minutes=timeMin)), str(timedelta(minutes=timeMax)),
                                         originalServiceTime, serviceTime,
                                         str(timedelta(minutes=timeMin + serviceTime)),
                                         str(timedelta(minutes=timeMax + serviceTime)),
                                         demand, capacity, previousLocationName])

                    index = assignment.Value(routing.NextVar(index))

    logging.info("Output csv file is written")





def logger(logging):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s %(process)d %(message)s',
                        #datefmt='%d/%m/%Y %I:%M:%S %p',
                        filename='../output/OptimizerLog.log', filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(levelname)s: %(asctime)s %(process)d %(message)s'))
    logging.getLogger().addHandler(console)