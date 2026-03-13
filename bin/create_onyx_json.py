#!/usr/bin/env python3

import pandas as pd
import sys
import os
import argparse
from pathlib import Path
import json
from onyx_analysis_helper import onyx_analysis_helper_functions as oa  # type: ignore


def get_id_names(in_path:str) -> [str, str]:
    climb_id = in_path.split("_")[0]
    run_id = in_path.split("_")[1]
    return climb_id, run_id


def load_report(in_path:str) -> pd.DataFrame:
    df = pd.read_csv(in_path,
                     sep="\t",
                     names=[
                         "percent_coverage",
                         "no_reads_covered",
                         "no_reads_assigned",
                         "rank",
                         "taxid",
                         "name"
                     ]
                    )
    return df


def load_results(in_path:str) ->pd.DataFrame:
    df_res = pd.read_csv(in_path,
                         sep="\t",
                         names=[
                             "isClassified",
                             "header",
                             "taxid",
                             "length",
                             "kmer_map"
                         ]
                        )
    return df_res


def create_analysis_fields(
    record_id: str,
    thresholds: dict,
    pipeline_info: dict,
    results: dict,  # Optional, needs to be a dictionary
    server: str,
    headline_result: str,  # Required
    result_folder: os.path,
) -> dict:
    """Set up fields dictionary used to populate analysis table containing
    QC metrics.
    Arguments:
        record_id -- Climb ID for sample
        thresholds -- thresholfs used in classification
        pipeline_info -- dictionary containing Name, Version and WebURL
        headline_result -- Short description of main result/virus presence TRUE or FALSE
        results -- Dictionary containing virus reclassification results
        server -- Server code is running on, one of "mscape" or "synthscape"
    Returns:
        onyx_analysis -- Class containing required fields for input to onyx
                         analysis table
        exitcode -- Exit code for checks - will be 0 if all checks passed, 1 if any checks failed
    """
    onyx_analysis = oa.OnyxAnalysis()
    onyx_analysis.add_analysis_details(
        analysis_name="gpha-mscape-orangebox-virus-reclassification",
        analysis_description="results from KRAKEN analysis rerun with a more complete representation of virus in utilsed database",
    )
    #onyx_analysis.add_package_metadata(package_name="mscape-sample-qc")
    onyx_analysis.pipeline_name = pipeline_info["name"]
    onyx_analysis.pipeline_version = pipeline_info["version"]
    onyx_analysis.pipeline_url = pipeline_info["homePage"]
    
    methods_fail = onyx_analysis.add_methods(methods_dict=thresholds)
    results_fail = onyx_analysis.add_results(top_result=headline_result, results_dict=results)
    onyx_analysis.add_server_records(sample_id=record_id, server_name=server)
    # output_fail = onyx_analysis.add_output_location(result_folder)
    required_field_fail, attribute_fail = onyx_analysis.check_analysis_object()
    
    # add in output fail to line below
    exitcode = 1 if any([methods_fail, results_fail, required_field_fail, attribute_fail]) else 0
    return onyx_analysis, exitcode


def write_onxy_results_to_json(results_dict: dict, climb_id: str, results_dir: os.path) -> os.path:
    """Write  results dictionary to json output file.
    Arguments:
        results_dict -- Dictionary containing results
        climb_id -- CLIMB ID to use in file name
        results_dir -- Directory to save results to
    Returns:
        os.path of saved json file
    """
    result_file = Path(results_dir) / f"{climb_id}.VIRUS_RECLASSIFICATION.analysis_fields.json"

    with Path(result_file).open("w") as file:
        json.dump(results_dict, file)

    return result_file



if __name__ == "__main__":
    """a main function"""
    parser = argparse.ArgumentParser(description="yes.")
    parser.add_argument('--report', type=str, required=True, help="path to Kraken report file")
    parser.add_argument('--results', type=str, required=True, help="path to Kraken results file")
    parser.add_argument('--results_json', type=str, required=True, help="path to the viral json file")
    parser.add_argument('--results_json_summary', type=str, required=True, help="path to the summary results json file")
    parser.add_argument('--climbid', type=str, required=False, help="climb id")
    parser.add_argument('--runid', type=str, required='--climb-id' in sys.argv, help="run id")
    parser.add_argument('--file_path', type=str, required=False, help="path to fastq file")
    parser.add_argument('--method', type=str, required=True, help="path to custom kraken database")
    parser.add_argument('--pipeline_info', type=str, required=True, help="pipeline infomation")
    
    args = parser.parse_args()
    
    print(args.pipeline_info)
    # Convert JSON String to Python dict
    with open(args.results_json) as json_file:
        results_json = json.load(json_file)
    with open(args.results_json_summary) as json_file:
        results_json_summary = json.load(json_file)

    pipeline_info_list = args.pipeline_info.split(",")
    pipeline_info_dict = {
        pipeline_info_list[0].split(":")[0]: pipeline_info_list[0].split(":")[1],  # Name
        pipeline_info_list[1].split(":")[0]: pipeline_info_list[1].split(":")[1],  # Version
        pipeline_info_list[2].split(":")[0]: ":".join(pipeline_info_list[2].split(":")[1:]),  # WebURL
    }
    
    analysis_fields_dict, exitcode = create_analysis_fields(record_id=args.climbid,
                                                  thresholds="",
                                                  pipeline_info=pipeline_info_dict,
                                                  results=results_json,  # Optional, needs to be a dictionary
                                                  server="mscape",
                                                  headline_result=results_json_summary,  # Required
                                                  result_folder="")
    analysis_fields_dict.write_analysis_to_json(f"{args.climbid}.VIRUS_RECLASSIFICATION.analysis_fields.json")
    