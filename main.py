from datetime import datetime
import os

from flask import Flask, request, jsonify
from flask import render_template
from flask import *
# from googleapiclient import discovery
# from oauth2client.client import GoogleCredentials

import handle_csv
import config

# credentials = GoogleCredentials.get_application_default()
# api = discovery.build("ml", "v1", credentials=credentials)


app = Flask(__name__)


def get_prediction(features, model_name,
                   version_name,
                   predict_key):
    project = config.project

    input_data = {"instances": [features]}

    # https://cloud.google.com/ai-platform/prediction/docs/online-predict#requesting_predictions
    parent = f"projects/{project}/models/{model_name}/versions/{version_name}"
    prediction = api.projects().predict(body=input_data, name=parent).execute()

    print(prediction)

    return prediction["predictions"][0][predict_key][0]


@app.route("/creditcard")
def creditcard():
    return render_template("creditcard.html")


@app.route("/")
@app.route("/usedcar")
def usedcar():
    maker = request.args.get('maker', None)
    model = request.args.get('model', None)
    if not model:
        if maker:
            model_list = handle_csv.get_models(maker)
            return jsonify(model_list)
    else:
        result = dict(
            fuelType=handle_csv.get_fuelTypes(model),
            transmission=handle_csv.get_transmission(model),
            mpg=handle_csv.get_mpg(model),
            engineSize=handle_csv.get_engineSize(model)
        )
        return jsonify(result)

    maker_list = handle_csv.get_makers('maker')
    return render_template("usedcar.html",
                           result='first', maker_list=maker_list)


@app.route("/usedcar/predict", methods=["GET", "POST"])
def predict():
    data = request.get_json()
    print(request.form)

    # maker = data.get('maker', None)
    # model = data.get('model', None)
    # fuelType = data.get('fueltype', None)
    # transmission = data.get('transmission', None)
    # mpg = data.get('mpg', None)
    # engineSize = data.get('enginesize', None)

    prediction = get_prediction(data,
                                config.model_name,
                                config.version_name,
                                config.predict_key)

    return "{:.1f} Pound(£)".format(prediction)


@app.route("/creditcard/predict", methods=["GET", "POST"])
def predict():
    data = request.get_json()
    print(request.form)

    # maker = data.get('maker', None)
    # model = data.get('model', None)
    # fuelType = data.get('fueltype', None)
    # transmission = data.get('transmission', None)
    # mpg = data.get('mpg', None)
    # engineSize = data.get('enginesize', None)

    prediction = get_prediction(data,
                                config.model_name,
                                config.version_name,
                                config.predict_key)

    return "{:.1f} Credit".format(prediction)


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
