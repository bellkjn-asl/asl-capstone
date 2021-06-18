import pandas as pd

df = pd.read_csv('car_spec.csv')


def get_makers(colname):
    return sorted(list(df[colname].unique()))


def get_models(maker):
    if maker:
        _df = df.loc[df['maker'] == maker.strip()]['Model']
    else:
        _df = df['Model']
    models = sorted(list(_df.unique()))
    models = [m.strip() for m in models]
    return models


def get_model_data(colname, model=None):
    if model:
        _df = df.loc[df['Model'].str.strip() == model.strip()]
    else:
        _df = df

    result = sorted(list(_df[colname].unique()))
    if _df[colname].dtype == 'object':
        result = [m.strip() for m in result]
    elif _df[colname].dtype == 'float':
        result = ['{:.1f}'.format(m) for m in result]

    return result


def get_years():
    return 1990, 2021


def get_fuelTypes(model=None):
    return get_model_data('FuelType', model)


def get_transmission(model=None):
    return get_model_data('Transmission', model)


def get_mpg(model=None):
    return get_model_data('Mpg', model)


def get_engineSize(model=None):
    return get_model_data('EngineSize', model)
