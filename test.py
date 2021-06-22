import main
import config

card_config = config.CREDIT_CARD

sample_data = {
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

result = main.get_prediction(sample_data,
                             card_config.model_name,
                             card_config.version_name,
                             card_config.predict_key)

print(result)
