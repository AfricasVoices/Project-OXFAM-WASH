from core_data_modules.cleaners import somali, swahili, Codes
from core_data_modules.cleaners.cleaning_utils import CleaningUtils
from core_data_modules.traced_data import Metadata
from core_data_modules.traced_data.util.fold_traced_data import FoldStrategies

from configuration import code_imputation_functions
from configuration.code_schemes import CodeSchemes
from src.lib.configuration_objects import CodingConfiguration, CodingModes, CodingPlan


def clean_age_with_range_filter(text):
    """
    Cleans age from the given `text`, setting to NC if the cleaned age is not in the range 10 <= age < 100.
    """
    age = swahili.DemographicCleaner.clean_age(text)
    if type(age) == int and 10 <= age < 100:
        return str(age)
        # TODO: Once the cleaners are updated to not return Codes.NOT_CODED, this should be updated to still return
        #       NC in the case where age is an int but is out of range
    else:
        return Codes.NOT_CODED


def get_rqa_coding_plans(pipeline_name):
    return [
        CodingPlan(raw_field="rqa_s01e01_raw",
                   time_field="sent_on",
                   run_id_field="rqa_s01e01_run_id",
                   coda_filename="OXFAM_WASH_s01e01.json",
                   icr_filename="s01e01.csv",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.MULTIPLE,
                           code_scheme=CodeSchemes.S01E01,
                           coded_field="rqa_s01e01_coded",
                           analysis_file_key="rqa_s01e01",
                           fold_strategy=lambda x, y: FoldStrategies.list_of_labels(CodeSchemes.S01E01, x, y)
                       )
                   ],
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value("OXFAM-WASH s01e01"),
                   raw_field_fold_strategy=FoldStrategies.concatenate),

        CodingPlan(raw_field="rqa_s01e02_raw",
                   time_field="sent_on",
                   run_id_field="rqa_s01e02_run_id",
                   coda_filename="OXFAM_WASH_s01e02.json",
                   icr_filename="s01e02.csv",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.MULTIPLE,
                           code_scheme=CodeSchemes.S01E02,
                           coded_field="rqa_s01e02_coded",
                           analysis_file_key="rqa_s01e02",
                           fold_strategy=lambda x, y: FoldStrategies.list_of_labels(CodeSchemes.S01E02, x, y)
                       )
                   ],
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value("OXFAM-WASH s01e02"),
                   raw_field_fold_strategy=FoldStrategies.concatenate),

        CodingPlan(raw_field="rqa_s01e03_raw",
                   time_field="sent_on",
                   run_id_field="rqa_s01e03_run_id",
                   coda_filename="OXFAM_WASH_s01e03.json",
                   icr_filename="s01e03.csv",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.MULTIPLE,
                           code_scheme=CodeSchemes.S01E03,
                           coded_field="rqa_s01e03_coded",
                           analysis_file_key="rqa_s01e03",
                           fold_strategy=lambda x, y: FoldStrategies.list_of_labels(CodeSchemes.S01E03, x, y)
                       )
                   ],
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value("OXFAM-WASH s01e03"),
                   raw_field_fold_strategy=FoldStrategies.concatenate),

        CodingPlan(raw_field="oxfam_beneficiary_consent_raw",
                   time_field="sent_on",
                   run_id_field="oxfam_beneficiary_consent_run_id",
                   coda_filename="OXFAM_WASH_Beneficiary_Consent.json",
                   icr_filename="oxfam_beneficiary_consent.csv",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.MULTIPLE,
                           code_scheme=CodeSchemes.BENEFICIARY_CONSENT,
                           coded_field="oxfam_beneficiary_consent_coded",
                           analysis_file_key="oxfam_beneficiary_consent",
                           fold_strategy=lambda x, y: FoldStrategies.list_of_labels(CodeSchemes.BENEFICIARY_CONSENT, x, y)
                       )
                   ],
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value("OXFAM WASH Beneficiary Consent"),
                   raw_field_fold_strategy=FoldStrategies.concatenate),

        CodingPlan(raw_field="rqa_s01e03_noise_handler_raw",
                   time_field="sent_on",
                   run_id_field="rqa_s01e03_noise_handler_run_id",
                   coda_filename="OXFAM_WASH_s01e03_Noise_Handler.json",
                   icr_filename="oxfam_wash_s01e03_noise_handler.csv",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.MULTIPLE,
                           code_scheme=CodeSchemes.S01E03_NOISE_HANDLER,
                           coded_field="rqa_s01e03_noise_handler_coded",
                           analysis_file_key="rqa_s01e03_s01e03_noise_handler",
                           fold_strategy=lambda x, y: FoldStrategies.list_of_labels(CodeSchemes.S01E03_NOISE_HANDLER, x, y)
                       )
                   ],
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value("OXFAM WASH s01e03 Noise Handler"),
                   raw_field_fold_strategy=FoldStrategies.concatenate),

        CodingPlan(raw_field="s01_close_out_raw",
                   time_field="sent_on",
                   run_id_field="s01_close_out_run_id",
                   coda_filename="OXFAM_WASH_s01_Close_Out.json",
                   icr_filename="oxfam_wash_s01_close_out.csv",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.MULTIPLE,
                           code_scheme=CodeSchemes.S01_CLOSE_OUT,
                           coded_field="s01_close_out_coded",
                           analysis_file_key="s01_close_out",
                           fold_strategy=lambda x, y: FoldStrategies.list_of_labels(CodeSchemes.S01_CLOSE_OUT, x,
                                                                                    y)
                       )
                   ],
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value("OXFAM WASH S01 Close Out"),
                   raw_field_fold_strategy=FoldStrategies.concatenate),

    ]

def get_demog_coding_plans(pipeline_name):
    return [
        CodingPlan(raw_field="gender_raw",
                   time_field="gender_time",
                   coda_filename="OXFAM_WASH_gender.json",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.SINGLE,
                           code_scheme=CodeSchemes.GENDER,
                           cleaner=somali.DemographicCleaner.clean_gender,
                           coded_field="gender_coded",
                           analysis_file_key="gender",
                           fold_strategy=FoldStrategies.assert_label_ids_equal
                       )
                   ],
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value("gender"),
                   raw_field_fold_strategy=FoldStrategies.assert_equal),

        CodingPlan(raw_field="age_raw",
                   time_field="age_time",
                   coda_filename="OXFAM_WASH_age.json",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.SINGLE,
                           code_scheme=CodeSchemes.AGE,
                           cleaner=clean_age_with_range_filter,
                           coded_field="age_coded",
                           analysis_file_key="age",
                           include_in_theme_distribution=Codes.FALSE,
                           fold_strategy=FoldStrategies.assert_label_ids_equal
                       ),
                       CodingConfiguration(
                           coding_mode=CodingModes.SINGLE,
                           code_scheme=CodeSchemes.AGE_CATEGORY,
                           coded_field="age_category_coded",
                           analysis_file_key="age_category",
                           fold_strategy=FoldStrategies.assert_label_ids_equal
                       )
                   ],
                   code_imputation_function=code_imputation_functions.impute_age_category,
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value("age"),
                   raw_field_fold_strategy=FoldStrategies.assert_equal),

        CodingPlan(raw_field="location_raw",
                   time_field="location_time",
                   coda_filename="OXFAM_WASH_location.json",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.SINGLE,
                           code_scheme=CodeSchemes.KENYA_COUNTY,
                           coded_field="county_coded",
                           analysis_file_key="county",
                           fold_strategy=FoldStrategies.assert_label_ids_equal
                       ),
                       CodingConfiguration(
                           coding_mode=CodingModes.SINGLE,
                           code_scheme=CodeSchemes.KENYA_CONSTITUENCY,
                           coded_field="constituency_coded",
                           analysis_file_key="constituency",
                           fold_strategy=FoldStrategies.assert_label_ids_equal
                       )
                   ],
                   code_imputation_function=code_imputation_functions.impute_kenya_location_codes,
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value("location"),
                   raw_field_fold_strategy=FoldStrategies.assert_equal),

        CodingPlan(raw_field="disabled_raw",
                   time_field="disabled_time",
                   coda_filename="OXFAM_WASH_disabled.json",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.SINGLE,
                           code_scheme=CodeSchemes.DISABLED,
                           coded_field="disabled_coded",
                           analysis_file_key="disabled",
                           fold_strategy=FoldStrategies.assert_label_ids_equal
                       )
                   ],
                ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value("disabled"),
                   raw_field_fold_strategy=FoldStrategies.assert_equal)
    ]

def get_follow_up_coding_plans(pipeline_name):
    return [
        CodingPlan(raw_field="rqa_s01_programme_evaluation_raw",
                   time_field="sent_on",
                   coda_filename="OXFAM_WASH_s01_Programme_Evaluation.json",
                   icr_filename="oxfam_programme_evaluation.csv",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.MULTIPLE,
                           code_scheme=CodeSchemes.S01_PROGRAMME_EVALUATION,
                           coded_field="rqa_s01_programme_evaluation_coded",
                           analysis_file_key="rqa_s01_programme_evaluation",
                           fold_strategy=lambda x, y: FoldStrategies.list_of_labels(
                               CodeSchemes.S01_PROGRAMME_EVALUATION, x,
                               y)
                       )
                   ],
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value(
                       "OXFAM WASH s01 Programme Evaluation"),
                   raw_field_fold_strategy=FoldStrategies.concatenate),

        CodingPlan(raw_field="rqa_s01_accountability_raw",
                   time_field="sent_on",
                   coda_filename="OXFAM_WASH_s01_Accountability.json",
                   run_id_field="rqa_s01_accountability_run_id",
                   icr_filename="oxfam_accountability.csv",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.MULTIPLE,
                           code_scheme=CodeSchemes.S01_ACCOUNTABILITY,
                           coded_field="rqa_s01_accountability_coded",
                           analysis_file_key="rqa_s01_accountability",
                           fold_strategy=lambda x, y: FoldStrategies.list_of_labels(
                               CodeSchemes.S01_ACCOUNTABILITY, x,
                               y)
                       )
                   ],
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value(
                       "OXFAM WASH s01 Accountability"),
                   raw_field_fold_strategy=FoldStrategies.concatenate),
    ]


def get_ws_correct_dataset_scheme(pipeline_name):
    return CodeSchemes.WS_CORRECT_DATASET
