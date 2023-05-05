from app import app
from model.get_model import get_model
obj=get_model()
@app.route("/get_report")
def get_controller():
    #calling get_model class's method
    return obj.get_model_method()