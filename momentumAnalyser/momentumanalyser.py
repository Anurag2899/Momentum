import os
import pandas as pd
from datetime import datetime, timedelta
from logger import logger
import threading

class MomentumAnalyser:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def process_data(self, symbol, df):
        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values(by='Date', inplace=True)
        today = datetime.today()
        one_month_ago = today - timedelta(days=30)
        three_months_ago = today - timedelta(days=90)
        six_months_ago = today - timedelta(days=180)
        twelve_months_ago = today - timedelta(days=365)
        momentum_data = {
            'Symbol': symbol,
            '1_month_momentum': df[df['Date'] >= one_month_ago]['Close'].pct_change(periods=1).mean(),
            '3_month_momentum': df[df['Date'] >= three_months_ago]['Close'].pct_change(periods=1).mean(),
            '6_month_momentum': df[df['Date'] >= six_months_ago]['Close'].pct_change(periods=1).mean(),
            '12_month_momentum': df[df['Date'] >= twelve_months_ago]['Close'].pct_change(periods=1).mean()
        }
        return momentum_data

    def process_and_save_data(self, symbol, df):
        momentum_data = self.process_data(symbol, df)
        self.results.append(momentum_data)

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
        self.results = []
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
        results_df = pd.DataFrame(self.results)
        file_path = os.path.join(self.output_dir, 'momentum_data.csv')
        try:
            results_df.to_csv(file_path, index=False)
            logger.info("Momentum analysis complete.")
        except Exception as e:
            logger.error(f"Error saving momentum data to {file_path}: {e}")
