import json

from core_data_modules.data_models import CodeScheme


def _open_scheme(filename):
    with open(f"code_schemes/{filename}", "r") as f:
        firebase_map = json.load(f)
        return CodeScheme.from_firebase_map(firebase_map)


class CodeSchemes(object):
    S01E01 = _open_scheme("s01e01.json")
    S01E02 = _open_scheme("s01e02.json")
    S01E03 = _open_scheme("s01e03.json")
    BENEFICIARY_CONSENT = _open_scheme("beneficiary_consent.json")
    S01E03_NOISE_HANDLER = _open_scheme("s01e03_noise_handler.json")
    S01_PROGRAMME_EVALUATION = _open_scheme("s01_programme_evaluation.json")
    S01_ACCOUNTABILITY = _open_scheme("s01_accountability.json")

    KENYA_CONSTITUENCY = _open_scheme("kenya_constituency.json")
    KENYA_COUNTY = _open_scheme("kenya_county.json")
    GENDER = _open_scheme("gender.json")
    AGE = _open_scheme("age.json")
    AGE_CATEGORY = _open_scheme("age_category.json")
    DISABLED = _open_scheme("disabled.json")

    WS_CORRECT_DATASET = _open_scheme("ws_correct_dataset.json")
