#!/usr/bin/env python3

import pandas as pd
import sys
import os
import argparse
from pathlib import Path
# from taxaplease.taxaplease import TaxaPlease
import json
#from utils import onyx_functions as of
#from onyx import OnyxConfig, OnyxClient, OnyxEnv, OnyxField
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
    record_id: str, reclassifier_methods: dict, headline_result: str, reclassification_results : dict, server: str
) -> dict:
    """Set up fields dictionary used to populate analysis table containing
    QC metrics.
    Arguments:
        record_id -- Climb ID for sample
        qc_thresholds -- Dictionary containing qc criteria used to generate metrics
        headline_result -- Short description of main result/virus presence TRUE or FALSE
        reclassification_results -- Dictionary containing virus reclassification results
        server -- Server code is running on, one of "mscape" or "synthscape"
    Returns:
        onyx_analysis -- Class containing required fields for input to onyx
                         analysis table
        exitcode -- Exit code for checks - will be 0 if all checks passed, 1 if any checks failed
    """
    onyx_analysis = oa.OnyxAnalysis()
    onyx_analysis.add_analysis_details(
        analysis_name="ukhsa-mscape-orangebox-virus-reclassification",
        analysis_description="results from KRAKEN analysis rerun with a more complete representation of virus in utilsed database",
    )
    onyx_analysis.add_package_metadata(package_name="mscape-virus-reclassification")
    methods_fail = onyx_analysis.add_methods(methods_dict=reclassifier_methods)
    results_fail = onyx_analysis.add_results(top_result=headline_result, results_dict=reclassification_results)
    onyx_analysis.add_server_records(sample_id=record_id, server_name=server)
    required_field_fail, attribute_fail = onyx_analysis.check_analysis_object(
        publish_analysis=False
    )

    if any([methods_fail, results_fail, required_field_fail, attribute_fail]): # noqa SIM108
        exitcode = 1
    else:
        exitcode = 0

    return onyx_analysis, exitcode


def write_onxy_results_to_json(results_dict: dict, climb_id: str, results_dir: os.path) -> os.path:
    """Write qc results dictionary to json output file.
    Arguments:
        qc_dict -- Dictionary containing qc results
        sample_id -- Sample ID to use in file name
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
    parser.add_argument('--json', type=str, required=True, help="path to the viral json file")
    parser.add_argument('--s3-bucket', type=str, required=True, help="path to s3-bucket")
    parser.add_argument('--climbid', type=str, required=False, help="climb id")
    parser.add_argument('--runid', type=str, required='--climb-id' in sys.argv, help="run id")
    parser.add_argument('--outdir', type=str, required=False, help="output directory path")
    parser.add_argument('--database', type=str, required=True, help='input databse path')
    
    args = parser.parse_args()
    df = load_report(in_path=args.report)
    
    results_dict = create_results_json(prefix=args.runid, 
                                       lineages=args.lineages, 
                                       bracken=args.bracken,
                                       report=args.report)
    
    analysis_fields_dict = create_analysis_fields(record_id=args.climbid,
                                                  reclassifier_methods="", 
                                                  headline_result=str(virus_presence(df_virus_genus)), 
                                                  # reclassification_results=results_dict, 
                                                  reclassification_results=args.json,
                                                  server="")
    
    write_onxy_results_to_json(results_dict=analysis_fields_dict,
                               climb_id=args.climbid,
                               results_dir=os.getcwd())
    