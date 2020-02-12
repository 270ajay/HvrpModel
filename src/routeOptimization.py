import data, utilities, optModel, logging




if __name__ == "__main__":

    try:
        utilities.logger(logging)
        logging.info("\n------------------------")

        data = data.getInputData()
        optModel.buildAndSolveOptimizationModel(data)

        logging.info("\n----------------------------------------------\n")



    except Exception as e:
        logging.exception('Optimization program failed')
        logging.info("\n----------------------------------------------\n")