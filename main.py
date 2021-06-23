import config
import handle_csv
from datetime import datetime
import os
import re
import random

from flask import Flask, request, jsonify
from flask import render_template
import logging
import sys

if sys.platform != 'win32':
    import cloud_logging
    from googleapiclient import discovery
    from oauth2client.client import GoogleCredentials

    credentials = GoogleCredentials.get_application_default()
    api = discovery.build("ml", "v1", credentials=credentials)


app = Flask(__name__)


SAMPLE_USEDCAR = {
    "manufacturer": "ford",
    "model": "ford Focus",
    "year": 2017,
    "transmission": "Manual",
    "fuelType": "Diesel",
    "mileage": 197,
    "tax": 145,
    "mpg": 74.3,
    "engineSize": 1.5
}

SAMPLE_CREDITCARD = {
    "gender": "M",
    "car": "Y",
    "reality": "N",
    "child_num": 0,
    "income_total": 112500.0,
    "income_type": "Pensioner",
    "edu_type": "Secondary / secondary special",
    "family_type": "Civil marriage",
    "house_type": "House / apartment",
    "DAYS_BIRTH": -21990,
    "DAYS_EMPLOYED": 365243,
    "work_phone": 0,
    "phone": 1,
    "email": 0,
    "occyp_type": "0",
    "family_size": 2.0,
    "begin_month": -60.0
}


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
    # making model prediction ready
    # card_config = config.CREDIT_CARD
    # prediction = get_prediction(SAMPLE_CREDITCARD,
    #                             card_config.model_name,
    #                             card_config.version_name,
    #                             card_config.predict_key)
    # logging.info(f'prediction: {prediction}')

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

    # making model prediction ready
    # usedcar_config = config.USED_CAR
    # prediction = get_prediction(SAMPLE_USEDCAR, usedcar_config.model_name,
    #                             usedcar_config.version_name, usedcar_config.predict_key)
    # logging.info(f'prediction: {prediction}')

    maker_list = handle_csv.get_makers()
    rand_idx = random.randint(0, len(maker_list)-1)
    selected_list = [''] * len(maker_list)
    selected_list[rand_idx] = 'selected'
    maker_dict = dict(zip(maker_list, selected_list))

    model_list = handle_csv.get_models(maker_list[rand_idx])

    fuelType = handle_csv.get_fuelTypes()
    transmission = handle_csv.get_transmission()
    mileage = dict(min=0.0, max=50.0, avg=25.0)
    tax = dict(min=0.0, max=1000.0, avg=500.0)

    mpg = handle_csv.get_mpg()
    _min = min(mpg)
    _max = max(mpg)
    _mid = round((_min+_max) / 2, 1)
    mpg = dict(min=_min, max=_max, avg=_mid)

    engineSize = handle_csv.get_engineSize()
    _min = min(engineSize)
    _max = max(engineSize)
    _mid = round((_min+_max) / 2, 1)
    engineSize = dict(min=_min, max=_max, avg=_mid)

    return render_template("usedcar.html",
                           maker_list=maker_dict,
                           model_list=model_list,
                           fuelType=fuelType,
                           transmission=transmission,
                           mpg=mpg,
                           engineSize=engineSize,
                           mileage=mileage,
                           tax=tax)


@app.route("/predict/usedcar", methods=["GET", "POST"])
def predict_usedcar():
    data = request.get_json()

    # maker = data.get('maker', None)
    # model = data.get('model', None)
    # fuelType = data.get('fueltype', None)
    # transmission = data.get('transmission', None)
    # mpg = data.get('mpg', None)
    # engineSize = data.get('enginesize', None)

    usedcar_config = config.USED_CAR

    prediction = get_prediction(data,
                                usedcar_config.model_name,
                                usedcar_config.version_name,
                                usedcar_config.predict_key)

    return "{:.1f} Pound(£)".format(prediction)


def is_number(s):
    return re.match(r'\d+(\.\d*)?', s)


def is_data_valid(data, sample):
    for k, v in sample.items():
        if k not in data:
            raise TypeError(f'{k} not in data')
        # if type(data[k]) != type(v):
        #     if isinstance(data[k], str):
        #         if is_number(data[k]):
        #             if isinstance(v, float):
        #                 data[k] = float(data[k])
        #             elif isinstance(v, int):
        #                 data[k] = int(data[k])
        #             else:
        #                 raise TypeError(
        #                     f'The type of {k} in data must be {type(v)}')

        #     else:
        #         raise TypeError(
        #             f'The type of {k} in data must be {type(v)}')


@app.route("/predict/creditcard", methods=["GET", "POST"])
def predict_creditcard():
    data = request.get_json()
    # data.pop('mobile')

    # sample_data = SAMPLE_CREDITCARD

    # is_data_valid(data, sample_data)

    # if data['DAYS_EMPLOYED'] == 365243:
    #     data['DAYS_EMPLOYED'] = 0
    # if data["DAYS_BIRTH"] > 0:
    #     data["DAYS_BIRTH"] = data["DAYS_BIRTH"] * -1
    # if data["DAYS_EMPLOYED"] > 0:
    #     data["DAYS_EMPLOYED"] = data["DAYS_EMPLOYED"] * -1
    # if data["begin_month"] > 0:
    #     data["begin_month"] = data["begin_month"] * -1

    card_config = config.CREDIT_CARD

    prediction = get_prediction(data,
                                card_config.model_name,
                                card_config.version_name,
                                card_config.predict_key)

    return f"{prediction} Credit"


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
