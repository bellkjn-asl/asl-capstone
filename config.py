project = "qwiklabs-gcp-04-0e6d92b4880a"


class creditcard_config():
    model_name = "credit_card"
    version_name = "baseline"
    predict_key = 'credit'


CREDIT_CARD = creditcard_config()


class usedcar_config():
    model_name = "used_car"
    version_name = "baseline"
    predict_key = 'price'


USED_CAR = usedcar_config()
