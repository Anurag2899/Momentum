import yfinance as yf
import pandas as pd
import os
import shutil
from multiprocessing import Pool
from logger import logger

class DataCollector:
    def __init__(self, equity_details_file, output_dir):
        self.equity_details_file = equity_details_file
        self.output_dir = output_dir

    def download_and_save_data(self, symbol):
        try:
            data = yf.download(f'{symbol}.NS', progress=False)  
            save_path = os.path.join(self.output_dir, f'{symbol}.csv')
            data.to_csv(save_path)
            # logger.info(f"Data downloaded and saved for {symbol}")
        except Exception as e:
            logger.error(f"Error downloading data for {symbol}: {e}")
            
    def collect_data(self):
        if not os.path.isfile(self.equity_details_file):
            logger.error("Equity details file not found.")
            return
        if os.path.exists(self.output_dir):
            logger.info(f"Deleting existing output directory '{self.output_dir}'")
            try:
                shutil.rmtree(self.output_dir)
                logger.info("Output directory deleted successfully")
            except Exception as e:
                logger.error(f"Error deleting output directory: {e}")
        os.makedirs(self.output_dir, exist_ok=True)
        equity_details = pd.read_csv(self.equity_details_file)
        with Pool() as pool:
            pool.map(self.download_and_save_data, equity_details['SYMBOL'])
            logger.info("Data collection complete")
