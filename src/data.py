import logging, excelFncs


def getInputData():

    logging.info("getting input data")
    data = {}

    dataFrames = excelFncs.readExcel('../input/InputData.xlsx')
    data['timeMatrix'] = excelFncs.readTimeMatrixSheet(dataFrames)
    data['vehicleDetails'] = excelFncs.readVehiclesSheet(dataFrames)
    data['orderDetails'] = excelFncs.readOrdersSheet(dataFrames, data['vehicleDetails'])
    data['modelParams'] = excelFncs.readModelSettingsSheet(dataFrames)

    logging.info("stored input data into objects")
    return data