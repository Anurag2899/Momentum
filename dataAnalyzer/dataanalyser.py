import os
import pandas as pd
from datetime import datetime, timedelta
from logger import logger
from multiprocessing import Pool
import threading


class DataAnalyser:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def process_data(self, symbol, df):
        today = datetime.today()
        start_date = today - timedelta(days=365)  
        df['Date'] = pd.to_datetime(df['Date'])
        df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= today)]
        file_path = os.path.join(self.output_dir, f'{symbol}.csv')
        try:
            df_filtered.to_csv(file_path, index=False)
            # logger.info(f"Processed data saved to {file_path}")
        except Exception as e:
            logger.error(f"Error saving processed data to {file_path}: {e}")

    def process_and_save_data(self, symbol, df):
        self.process_data(symbol, df)

    def process_all_data(self):
        if os.path.exists(self.output_dir):
            for filename in os.listdir(self.output_dir):
                file_path = os.path.join(self.output_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        # logger.info(f"Deleted existing file: {file_path}")
                except Exception as e:
                    logger.error(f"Error deleting file: {file_path}: {e}")
        else:
            os.makedirs(self.output_dir, exist_ok=True)
            logger.info(f"Created directory: {self.output_dir}")

        data = {}
        for filename in os.listdir(self.input_dir):
            if filename.endswith('.csv'):
                symbol = os.path.splitext(filename)[0]
                file_path = os.path.join(self.input_dir, filename)
                try:
                    df = pd.read_csv(file_path)
                    data[symbol] = df
                    # logger.info(f"Read data from {filename}")
                except Exception as e:
                    logger.error(f"Error reading data from {filename}: {e}")

        threads = []
        for symbol, df in data.items():
            thread = threading.Thread(target=self.process_and_save_data, args=(symbol, df))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
        logger.info("Data processing complete")