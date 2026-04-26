import sys
import pandas as pd
from src.logger import logging
from src.exception import MyException
from src.utils.main_utils import load_object
from src.constants import MODEL_FILE_NAME, ARTIFACTS_DIR
import os


class VehicleData:
    """
    User se jo data aayega usse yahan store karenge.
    Flask app se yahi class use hogi.
    """
    def __init__(
        self,
        make: str,
        model: str,
        year: int,
        vehicle_type: str,
        fuel_type: str,
        transmission: str,
        mileage_kmpl: float,
        engine_cc: float,
        max_power_bhp: float,
        seats: int,
        age_years: int
    ):
        self.make = make
        self.model = model
        self.year = year
        self.vehicle_type = vehicle_type
        self.fuel_type = fuel_type
        self.transmission = transmission
        self.mileage_kmpl = mileage_kmpl
        self.engine_cc = engine_cc
        self.max_power_bhp = max_power_bhp
        self.seats = seats
        self.age_years = age_years

    def get_data_as_dataframe(self) -> pd.DataFrame:
        """
        User ka data DataFrame mein convert karta hai
        taaki model predict kar sake.
        """
        try:
            data = {
                "make"          : [self.make],
                "model"         : [self.model],
                "year"          : [self.year],
                "type"          : [self.vehicle_type],
                "fuel_type"     : [self.fuel_type],
                "transmission"  : [self.transmission],
                "mileage_kmpl"  : [self.mileage_kmpl],
                "engine_cc"     : [self.engine_cc],
                "max_power_bhp" : [self.max_power_bhp],
                "seats"         : [self.seats],
                "age_years"     : [self.age_years]
            }
            df = pd.DataFrame(data)
            logging.info(f"User data DataFrame bana: {df}")
            return df

        except Exception as e:
            raise MyException(e, sys)


class PredictionPipeline:
    """
    Trained model load karke price predict karta hai.
    """

    def __init__(self):
        pass

    def get_latest_model_path(self) -> str:
        """
        Sabse latest artifacts folder se model path dhundhta hai.
        """
        try:
            all_artifacts = os.listdir(ARTIFACTS_DIR)
            latest_artifact = sorted(all_artifacts)[-1]

            model_path = os.path.join(
                ARTIFACTS_DIR,
                latest_artifact,
                "model_trainer",
                MODEL_FILE_NAME
            )

            logging.info(f"Latest model path: {model_path}")
            return model_path

        except Exception as e:
            raise MyException(e, sys)

    def predict(self, dataframe: pd.DataFrame) -> float:
        try:                                              # ← 8 spaces indent
            logging.info("========== Prediction Shuru ==========")

            # Latest model load karo
            model_path = self.get_latest_model_path()
            model = load_object(model_path)

            # Model ne jin columns par train kiya tha wahi use karo
            training_columns = model.feature_names_in_

            # Sirf numeric columns rakhho
            numeric_df = dataframe.select_dtypes(include=['number'])

            # Missing columns ko 0 se fill karo
            for col in training_columns:
                if col not in numeric_df.columns:
                    numeric_df[col] = 0

            # Sirf training wale columns use karo same order mein
            numeric_df = numeric_df[training_columns]

            # Prediction karo
            prediction = model.predict(numeric_df)
            price = round(prediction[0], 2)

            logging.info(f"Predicted Price: ₹{price}")
            logging.info("========== Prediction Complete ==========")

            return price

        except Exception as e:                           # ← 8 spaces indent
            raise MyException(e, sys)