from pandas import read_excel


def readExcel(fileName):
    dataFrames = read_excel(fileName, sheetname=None)
    return dataFrames




def initializeAndUpdateOrderDetailsWithDepotInfo(depotInfo):

    orderDetails = {}
    orderDetails['orderList'] = []
    orderDetails['locationList'] = []
    orderDetails['demandList'] = []
    orderDetails['serviceTime'] = []
    orderDetails['costOfNotServingList'] = []
    orderDetails['minEntryTimeList'] = []
    orderDetails['maxEntryTimeList'] = []

    for depot in depotInfo:
        orderDetails['orderList'].append('')
        orderDetails['locationList'].append(depot)
        orderDetails['demandList'].append(0)
        orderDetails['serviceTime'].append(0)
        orderDetails['costOfNotServingList'].append(0)
        orderDetails['minEntryTimeList'].append(0)
        orderDetails['maxEntryTimeList'].append(0)

    return orderDetails





def readOrdersSheet(dataFrames, vehicleDetails):

    dataFrame = dataFrames["Orders"]
    dataFrame = dataFrame.dropna()
    orderDetails = initializeAndUpdateOrderDetailsWithDepotInfo(vehicleDetails['depotInfo'])

    dataFrame['Order'].astype(str)
    dataFrame['Location'].astype(str)
    dataFrame['Demand'].astype(int)
    dataFrame['ServiceTime'].astype(int)
    dataFrame['CostOfNotServing'].astype(int)
    dataFrame['MinEntryTime'].astype(int)
    dataFrame['MaxEntryTime'].astype(int)


    orderDetails['orderList'] += dataFrame['Order'].tolist()
    orderDetails['locationList'] += dataFrame['Location'].tolist()
    orderDetails['demandList'] += dataFrame['Demand'].tolist()
    orderDetails['serviceTime'] += dataFrame['ServiceTime'].tolist()
    orderDetails['costOfNotServingList'] += dataFrame['CostOfNotServing'].tolist()
    orderDetails['minEntryTimeList'] += dataFrame['MinEntryTime'].tolist()
    orderDetails['maxEntryTimeList'] += dataFrame['MaxEntryTime'].tolist()

    orderDetails['numOfNodes'] = len(orderDetails['locationList'])
    return orderDetails




def readVehiclesSheet(dataFrames):

    vehicleDetails = {}
    dataFrame = dataFrames["Vehicles"]
    dataFrame = dataFrame.dropna()

    dataFrame['VehicleName'].astype(str)
    dataFrame['Cost'].astype(int)
    dataFrame['Capacity'].astype(int)
    dataFrame['ServiceTimeFactor'].astype(float)
    dataFrame['SpeedFactor'].astype(float)
    dataFrame['MinStartTime'].astype(int)
    dataFrame['MaxStartTime'].astype(int)
    dataFrame['MaxEndTime'].astype(int)
    dataFrame['MaxWorkingHours'].astype(int)

    vehicleDetails['vehicleNameList'] = dataFrame['VehicleName'].tolist()
    vehicleDetails['costList'] = dataFrame['Cost'].tolist()
    vehicleDetails['capacityList'] = dataFrame['Capacity'].tolist()
    vehicleDetails['serviceTimeFactorList'] = dataFrame['ServiceTimeFactor'].tolist()
    vehicleDetails['speedFactorList'] = dataFrame['SpeedFactor'].tolist()
    vehicleDetails['minStartTimeList'] = dataFrame['MinStartTime'].tolist()
    vehicleDetails['maxStartTimeList'] = dataFrame['MaxStartTime'].tolist()
    vehicleDetails['maxEndTimeList'] = dataFrame['MaxEndTime'].tolist()
    vehicleDetails['maxWorkingHoursList'] = dataFrame['MaxWorkingHours'].tolist()
    vehicleDetails['numOfVehicles'] = len(vehicleDetails['vehicleNameList'])
    vehicleDetails['startDepotIndices'] = []
    vehicleDetails['endDepotIndices'] = []

    startDepotList = dataFrame['StartDepot'].tolist()
    endDepotList  = dataFrame['EndDepot'].tolist()
    vehicleDetails['depotInfo'] = list(set(startDepotList + endDepotList))

    for i in range(vehicleDetails['numOfVehicles']):
        vehicleDetails['startDepotIndices'].append(vehicleDetails['depotInfo'].index(startDepotList[i]))
        vehicleDetails['endDepotIndices'].append(vehicleDetails['depotInfo'].index(endDepotList[i]))

    return  vehicleDetails





def readTimeMatrixSheet(dataFrames):

    dataFrame = dataFrames['TimeMatrix']
    dataFrame = dataFrame.dropna()
    dataFrame = dataFrame.applymap(lambda x: round(x))
    timeMatrix = dataFrame.T.to_dict()
    return timeMatrix




def readModelSettingsSheet(dataFrames):

    modelParams = {}

    dataFrame = dataFrames["ModelSettings"]
    valueList = dataFrame['Value'].tolist()

    modelParams['solverTimeLimit'] = int(valueList[0])
    modelParams['displaySolverSearch'] = int(valueList[1])
    modelParams['maxWaiting'] = int(valueList[2])

    return modelParams