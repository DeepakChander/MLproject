import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd  # type: ignore

from sklearn.model_selection import train_test_split  # type: ignore
from dataclasses import dataclass


@dataclass
class DataIngestionconfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "raw.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionconfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")

        try:
            # Correct file path using raw string
            df = pd.read_csv(r'notebooks\data\stud.csv')
            logging.info('Read the dataset as DataFrame')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train test split initiates")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the data is completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys) from e


if __name__ == "__main__":  # Fixed comparison syntax here
    obj = DataIngestion()
    obj.initiate_data_ingestion()