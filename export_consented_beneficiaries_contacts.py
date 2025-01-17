import argparse
import csv
import json

from core_data_modules.cleaners import Codes
from core_data_modules.logging import Logger
from core_data_modules.traced_data.io import TracedDataJsonIO
from id_infrastructure.firestore_uuid_table import FirestoreUuidTable
from storage.google_cloud import google_cloud_utils

from src.lib import PipelineConfiguration

log = Logger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates lists of beneficiaries phone numbers to advertise to using project "
                                                 "traced data and KK exclusion lists")

    parser.add_argument("--exclusion-list-file-path", nargs="?",
                        help="List of phone numbers to exclude from the ad group")
    parser.add_argument("google_cloud_credentials_file_path", metavar="google-cloud-credentials-file-path",
                        help="Path to a Google Cloud service account credentials file to use to access the "
                             "credentials bucket")
    parser.add_argument("pipeline_configuration_file_path", metavar="pipeline-configuration-file",
                        help="Path to the pipeline configuration json file")
    parser.add_argument("traced_data_paths", metavar="traced-data-paths", nargs="+",
                        help="Paths to the traced data files (either messages or individuals) to extract phone "
                             "numbers from")
    parser.add_argument("csv_output_file_path", metavar="csv-output-file-path",
                        help="Path to a CSV file to write the beneficiaries contacts too. "
                             "Exported file is in a format suitable for direct upload to Rapid Pro")

    args = parser.parse_args()

    exclusion_list_file_path = args.exclusion_list_file_path
    google_cloud_credentials_file_path = args.google_cloud_credentials_file_path
    pipeline_configuration_file_path = args.pipeline_configuration_file_path
    traced_data_paths = args.traced_data_paths
    csv_output_file_path = args.csv_output_file_path

    log.info("Loading Pipeline Configuration File...")
    with open(pipeline_configuration_file_path) as f:
        pipeline_configuration = PipelineConfiguration.from_configuration_file(f)
    Logger.set_project_name(pipeline_configuration.pipeline_name)
    log.debug(f"Pipeline name is {pipeline_configuration.pipeline_name}")

    log.info("Downloading Firestore UUID Table credentials...")
    firestore_uuid_table_credentials = json.loads(google_cloud_utils.download_blob_to_string(
        google_cloud_credentials_file_path,
        pipeline_configuration.phone_number_uuid_table.firebase_credentials_file_url
    ))

    phone_number_uuid_table = FirestoreUuidTable(
        pipeline_configuration.phone_number_uuid_table.table_name,
        firestore_uuid_table_credentials,
        "avf-phone-uuid-"
    )
    log.info("Initialised the Firestore UUID table")

    consented_beneficiaries_uuids = set()
    for path in traced_data_paths:
        # Load the traced data
        log.info(f"Loading previous traced data from file '{path}'...")
        with open(path) as f:
            data = TracedDataJsonIO.import_jsonl_to_traced_data_iterable(f)
        log.info(f"Loaded {len(data)} traced data objects")

        for td in data:
            if td["consent_withdrawn"] == Codes.TRUE:
                continue

            if td['beneficiary'] == Codes.TRUE:
                consented_beneficiaries_uuids.add(td["uid"])

    if exclusion_list_file_path is not None:
        # Load the exclusion list
        log.info(f"Loading the exclusion list from {exclusion_list_file_path}...")
        with open(exclusion_list_file_path) as f:
            exclusion_list = json.load(f)
        log.info(f"Loaded {len(exclusion_list)} numbers to exclude")

        # Remove any uuids in the exclusion list
        log.info(f"Removing exclusion list uuids from the contacts group")
        removed = 0
        for uuid in exclusion_list:
            if uuid in consented_beneficiaries_uuids:
                removed += 1
                consented_beneficiaries_uuids.remove(uuid)
        log.info(f"Removed {removed} uuids; {len(consented_beneficiaries_uuids)} remain")

    # Convert the uuids to phone numbers
    log.info(f"Converting {len(consented_beneficiaries_uuids)} uuids to phone numbers...")
    uuid_phone_number_lut = phone_number_uuid_table.uuid_to_data_batch(consented_beneficiaries_uuids)
    phone_numbers = set()

    # Export contacts CSV
    log.warning(f"Exporting {len(phone_numbers)} phone numbers to {csv_output_file_path}...")
    with open(csv_output_file_path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=["URN:Tel", "Name"], lineterminator="\n")
        writer.writeheader()

        for n in phone_numbers:
            writer.writerow({
                "URN:Tel": n
            })
        log.info(f"Wrote {len(phone_numbers)} contacts to {csv_output_file_path}")
