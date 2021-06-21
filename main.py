from datetime import datetime
import os

from flask import Flask, request, jsonify
from flask import render_template
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

import handle_csv
import config

credentials = GoogleCredentials.get_application_default()
api = discovery.build("ml", "v1", credentials=credentials)


app = Flask(__name__)


def get_prediction(features,
                   model_name,
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


@app.route("/sample")
def sample():

    return render_template("sample.html")


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

    maker_list = handle_csv.get_makers()
    fuelType = handle_csv.get_fuelTypes()
    transmission = handle_csv.get_transmission()
    mileage = dict(min=0.0, max=50.0)

    mpg = handle_csv.get_mpg()
    mpg = dict(min=min(mpg), max=max(mpg))

    engineSize = handle_csv.get_engineSize()
    engineSize = dict(min=min(engineSize), max=max(engineSize))

    return render_template("usedcar.html",
                           result='first',
                           maker_list=maker_list,
                           fuelType=fuelType,
                           transmission=transmission,
                           mpg=mpg,
                           engineSize=engineSize,
                           mileage=mileage)


@app.route("/predict/usedcar", methods=["GET", "POST"])
def predict_usedcar():
    data = request.get_json()

    # "manufacturer": "ford",
    # "model": "ford Focus",
    # "year": 2017,
    # "transmission": "Manual",
    # "fuelType": "Diesel",
    # "mileage": 197,
    # "tax": 145,
    # "mpg": 74.3,
    # "engineSize": 1.5

    # maker = data.get('maker', None)
    # model = data.get('model', None)
    # fuelType = data.get('fueltype', None)
    # transmission = data.get('transmission', None)
    # mpg = data.get('mpg', None)
    # engineSize = data.get('enginesize', None)
    data['year'] = data.pop('carYear')
    data['manufacturer'] = data.pop('maker')
    data['engineSize'] = data.pop('engine')
    data["mileage"] = float(data["mileage"])
    data["tax"] = float(data["tax"])
    data["mpg"] = float(data["mpg"])
    data["engineSize"] = float(data["engineSize"])

    usedcar_config = config.USED_CAR

    prediction = get_prediction(data,
                                usedcar_config.model_name,
                                usedcar_config.version_name,
                                usedcar_config.predict_key)

    return "{:.1f} Pound(£)".format(prediction)


@app.route("/predict/creditcard", methods=["GET", "POST"])
def predict_creditcard():
    data = request.get_json()

    card_config = config.CREDIT_CARD

    prediction = get_prediction(data,
                                card_config.model_name,
                                card_config.version_name,
                                card_config.predict_key)

    return "{:.1f} Credit".format(prediction)


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
