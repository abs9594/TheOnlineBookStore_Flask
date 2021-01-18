from flask import Blueprint,request,jsonify,render_template
from ml_modeling.predict import make_prediction
from api.forms import FoodReviewForm
import json
prediction_app = Blueprint('prediction_app',__name__)

@prediction_app.route("/",methods=['GET'])
def home():
	if request.method == 'GET':
		return render_template('home.html')

@prediction_app.route('/v1/predict/', methods=['POST','GET'])
def predict():
    if request.method == 'POST':
        try:
            json_data = request.get_json()
        except Exception as err:
            pass
        
        try:
            # print(request.form)
            json_data = {}
            json_data["Text"] = request.form.get("text")
            json_data["Summary"] = request.form.get("summary")
        except Exception as err:
            pass
        # print(f'Inputs: {json_data}')

        result = make_prediction(input_data=json_data)
        # print(f'Outputs: {result}')
        # print(result['predictions'][0])

        predictions = result.get('predictions')[0]
        # version = result.get('version')
        review = "Positive" if predictions else "negative"
        # return jsonify({'predictions': review})
        return render_template("prediction/predictionResult.html",prediction=review)

    elif request.method == "GET":
        form = FoodReviewForm()
        return render_template('prediction/foodreviewform.html',form=form)
