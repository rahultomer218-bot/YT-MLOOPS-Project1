from flask import Flask, render_template, request
import sys
from src.logger import logging
from src.exception import MyException
from src.pipeline.prediction_pipeline import PredictionPipeline, VehicleData

app = Flask(__name__)


# ============================================================
# HOME PAGE
# ============================================================
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# ============================================================
# PREDICTION PAGE
# ============================================================
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return render_template("predict.html")

    if request.method == "POST":
        try:
            # User ka data form se lo
            vehicle_data = VehicleData(
                make            = request.form.get("make"),
                model           = request.form.get("model"),
                year            = int(request.form.get("year")),
                vehicle_type    = request.form.get("vehicle_type"),
                fuel_type       = request.form.get("fuel_type"),
                transmission    = request.form.get("transmission"),
                mileage_kmpl    = float(request.form.get("mileage_kmpl")),
                engine_cc       = float(request.form.get("engine_cc")),
                max_power_bhp   = float(request.form.get("max_power_bhp")),
                seats           = int(request.form.get("seats")),
                age_years       = int(request.form.get("age_years"))
            )

            # DataFrame banao
            df = vehicle_data.get_data_as_dataframe()

            # Prediction karo
            pipeline = PredictionPipeline()
            predicted_price = pipeline.predict(df)

            logging.info(f"Predicted Price: ₹{predicted_price}")

            return render_template(
                "predict.html",
                predicted_price=f"₹ {predicted_price:,.2f}"
            )

        except Exception as e:
            logging.error(f"Prediction mein error: {e}")
            raise MyException(e, sys)


# ============================================================
# TRAINING PIPELINE TRIGGER
# ============================================================
@app.route("/train", methods=["GET"])
def train():
    try:
        from src.pipeline.training_pipeline import TrainingPipeline
        pipeline = TrainingPipeline()
        pipeline.run_pipeline()
        return "✅ Training Pipeline Successfully Complete Ho Gayi!"
    except Exception as e:
        raise MyException(e, sys)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)