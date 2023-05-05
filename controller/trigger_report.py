from datetime import datetime, timedelta
from pytz import timezone
from flask import Flask, jsonify
from model.trigger_model import TriggerModel

app = Flask(__name__)

obj = TriggerModel()

@app.route("/trigger_report")
def trigger_controller():
    result = obj.trigger_model_method()

    # Generate report ID based on the current UTC timestamp
    report_id = datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")

    # Generate the report data in JSON format
    report_data = {
        "report_id": report_id,
        "timestamp_utc": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "report": result
    }

    return jsonify(report_data)