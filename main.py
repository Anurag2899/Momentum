from dataCollector.datacollector import DataCollector
from dataAnalyzer.dataanalyser import DataAnalyser
from momentumAnalyser.momentumanalyser import MomentumAnalyser
from constants.constants import Constants
from logger import logger
import time

def main():
    start_time = time.time()

    logger.info("Starting data collection")
    LOS = Constants.LIST_OF_ALL_STOCKS_INDIA
    HDSD = Constants.HISTORICAL_DATA_SAVE_DIR
    collector = DataCollector(LOS, HDSD)
    collector.collect_data()

    logger.info("Starting data analysis")
    ADSD = Constants.ANALYSED_DATA_SAVE_DIR
    analyser = DataAnalyser(HDSD, ADSD)
    analyser.process_all_data()

    logger.info("Starting MOMENTUM analysis")
    MDSD = Constants.MOMENTUM_DATA_SAVE_DIR
    momentum = MomentumAnalyser(ADSD, MDSD)
    momentum.process_all_data()

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Total time taken: {elapsed_time} seconds")

if __name__ == "__main__":
    main()
