project = "qwiklabs-gcp-04-0e6d92b4880a"


class creditcard_config():
    model_name = "credit_card_model"
    version_name = "v4"
    predict_key = 'prediction'


CREDIT_CARD = creditcard_config()


class usedcar_config():
    model_name = "used_car"
    version_name = "jbm_test"
    predict_key = 'price'


USED_CAR = usedcar_config()
