project = "qwiklabs-gcp-00-0db9b1bc58c6"


class creditcard_config():
    model_name = "babyweight2"
    version_name = "ml_on_gcp"
    predict_key = 'output'


CREDIT_CARD = creditcard_config()


class usedcar_config():
    model_name = "used_car"
    version_name = "baseline"
    predict_key = 'price'


USED_CAR = usedcar_config()
