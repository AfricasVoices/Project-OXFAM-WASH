import csv
from collections import OrderedDict
import sys
import time

from core_data_modules.cleaners import Codes
from core_data_modules.traced_data import Metadata
from core_data_modules.traced_data.util import FoldTracedData
from core_data_modules.traced_data.util.fold_traced_data import FoldStrategies

from src.lib import PipelineConfiguration, ConsentUtils
from src.lib.configuration_objects import CodingModes

class AnalysisFile(object):
    @staticmethod
    def tag_beneficiary_participants(user, data, pipeline_configuration, raw_data_dir):
        """
        This tags uids who are our partners beneficiaries.
        :param user: Identifier of the user running this program, for TracedData Metadata.
        :type user: str
        :param data: TracedData objects to tag listening group participation to.
        :type data: iterable of TracedData
        :param raw_data_dir: Directory containing de-identified beneficiary contacts CSVs containing
                                    beneficiary data stored as `avf-phone-uuid` and `location` columns.
        :type user: str
        :param pipeline_configuration: Pipeline configuration.
        :type pipeline_configuration: PipelineConfiguration
        """
        beneficiary_uids = set()  # Contains avf-phone ids of partner's beneficiaries.

        # Read beneficiary file CSVs data
        for beneficiary_file_url in pipeline_configuration.beneficiary_file_urls:
            with open(f'{raw_data_dir}/{beneficiary_file_url.split("/")[-1]}', "r", encoding='utf-8-sig') as f:
                beneficiary_data = list(csv.DictReader(f))
                for row in beneficiary_data:
                    beneficiary_uids.add(row['avf-phone-uuid'])

        # 1.Check if a participant is part of the beneficiary contacts then tag true or false otherwise
        #   Example - "beneficiary": true
        for td in data:
            beneficiary_data = dict()  # of uid repeat and weekly listening group participation data
            beneficiary_data["beneficiary"] = td["uid"] in beneficiary_uids

            td.append_data(beneficiary_data, Metadata(user, Metadata.get_call_location(), time.time()))

    @staticmethod
    def export_to_csv(user, data, csv_path, export_keys, consent_withdrawn_key):
        with open(csv_path, "w") as f:
            writer = csv.DictWriter(f, fieldnames=export_keys, lineterminator="\n")
            writer.writeheader()

            for td in data:
                analysis_dict = dict()

                # If consent was withdrawn, export the uid and consent_withdrawn_key.
                # Export "STOP" for every other variable.
                if td[consent_withdrawn_key] == Codes.TRUE:
                    analysis_dict = {k: Codes.STOP for k in export_keys}
                    analysis_dict["uid"] = td["uid"]
                    analysis_dict[consent_withdrawn_key] = td[consent_withdrawn_key]
                    writer.writerow(analysis_dict)
                    continue

                # Convert codes to their string/matrix values for export.
                for plan in PipelineConfiguration.RQA_CODING_PLANS + PipelineConfiguration.SURVEY_CODING_PLANS:
                    for cc in plan.coding_configurations:
                        if cc.analysis_file_key is None:
                            continue

                        if cc.coding_mode == CodingModes.SINGLE:
                            analysis_dict[cc.analysis_file_key] = \
                                cc.code_scheme.get_code_with_code_id(td[cc.coded_field]["CodeID"]).string_value
                        else:
                            assert cc.coding_mode == CodingModes.MULTIPLE
                            show_matrix_keys = []
                            for code in cc.code_scheme.codes:
                                show_matrix_keys.append(f"{cc.analysis_file_key}_{code.string_value}")

                            for label in td[cc.coded_field]:
                                code_string_value = cc.code_scheme.get_code_with_code_id(label["CodeID"]).string_value
                                analysis_dict[f"{cc.analysis_file_key}_{code_string_value}"] = Codes.MATRIX_1

                            for key in show_matrix_keys:
                                if key not in analysis_dict:
                                    analysis_dict[key] = Codes.MATRIX_0

                # Prepare all the other values, which don't need converting to strings, for export.
                for key in export_keys:
                    if key not in analysis_dict and key in td:
                        analysis_dict[key] = td[key]

                writer.writerow(analysis_dict)

    @classmethod
    def generate(cls, user, data, pipeline_configuration, raw_data_dir, csv_by_message_output_path, csv_by_individual_output_path):
        # Serializer is currently overflowing
        # TODO: Investigate/address the cause of this.
        sys.setrecursionlimit(15000)

        # Set consent withdrawn based on presence of data coded as "stop"
        consent_withdrawn_key = "consent_withdrawn"
        ConsentUtils.determine_consent_withdrawn(
            user, data, PipelineConfiguration.RQA_CODING_PLANS + PipelineConfiguration.SURVEY_CODING_PLANS,
            consent_withdrawn_key
        )

        # Set the list of keys to be exported and how they are to be handled when folding
        fold_strategies = OrderedDict()
        fold_strategies["uid"] = FoldStrategies.assert_equal
        fold_strategies[consent_withdrawn_key] = FoldStrategies.boolean_or

        export_keys = ["uid", consent_withdrawn_key, "beneficiary"]

        for plan in PipelineConfiguration.RQA_CODING_PLANS + PipelineConfiguration.SURVEY_CODING_PLANS:
            for cc in plan.coding_configurations:
                if cc.analysis_file_key is None:
                    continue

                if cc.coding_mode == CodingModes.SINGLE:
                    export_keys.append(cc.analysis_file_key)
                else:
                    assert cc.coding_mode == CodingModes.MULTIPLE
                    for code in cc.code_scheme.codes:
                        export_keys.append(f"{cc.analysis_file_key}_{code.string_value}")

                fold_strategies[cc.coded_field] = cc.fold_strategy

            export_keys.append(plan.raw_field)
            fold_strategies[plan.raw_field] = plan.raw_field_fold_strategy

        # Fold data to have one respondent per row
        to_be_folded = []
        for td in data:
            to_be_folded.append(td.copy())

        folded_data = FoldTracedData.fold_iterable_of_traced_data(
            user, to_be_folded, lambda td: td["uid"], fold_strategies
        )

        ConsentUtils.set_stopped(user, data, consent_withdrawn_key)
        ConsentUtils.set_stopped(user, folded_data, consent_withdrawn_key)

        # Tag listening group participants
        cls.tag_beneficiary_participants(user, data, pipeline_configuration, raw_data_dir)
        cls.tag_beneficiary_participants(user, folded_data, pipeline_configuration, raw_data_dir)

        cls.export_to_csv(user, data, csv_by_message_output_path, export_keys, consent_withdrawn_key)
        cls.export_to_csv(user, folded_data, csv_by_individual_output_path, export_keys, consent_withdrawn_key)

        return data, folded_data
