#!/usr/bin/env python3

import pandas as pd
import sys
import os
import argparse
from pathlib import Path
from taxaplease.taxaplease import TaxaPlease
import json
# from utils import onyx_functions as of
# from onyx import OnyxConfig, OnyxClient, OnyxEnv, OnyxField

"""Script to create an aggregated count from lineage data."""
### taken from epi2ome/wf-metagenomics under the conditions of their license https://github.com/epi2me-labs/wf-metagenomics/blob/master/LICENSE and modified for this use case. copied from scylla https://github.com/artic-network/scylla/blob/2bbc52aa36811d8ab36918e4eda2f83b17d62a13/bin/aggregate_lineages_bracken.py 

UNCLASSIFIED = "Unclassified"
UNKNOWN = "Unknown"

RANKS = [
    "superkingdom",
    "clade",
    "kingdom",
    "phylum",
    "subphylum",
    "class",
    "order",
    "family",
    "genus",
    "species",
    "subspecies",
    "serotype",
]


def update_or_create_unclassified(entries, unclassified_count):
    """Handle unclassified entries."""
    entries[UNCLASSIFIED] = {
        "taxid": 0,
        "rank": RANKS[0],
        "count": int(unclassified_count),
        "children": {
            UNKNOWN: {
                "taxid": 0,
                "rank": "species",
                "count": int(unclassified_count),
                "children": {},
            }
        },
    }
    return entries


def update_or_create_count(entry, entries, bracken_counts):
    """Increment lineage counts given entries."""
    taxid, lineage, ranks = entry.rstrip().split("\t")
    lineage_split = lineage.split(";")
    ranks_split = ranks.split(";")
    count = int(bracken_counts[taxid])

    previous = entries
    previous_rank = None
    for [name, rank] in zip(lineage_split, ranks_split):

        if rank not in RANKS:
            if previous_rank == "species":
                rank = "subspecies"
            else:
                continue

        current = previous.get(name)
        if not current:
            new_entry = {"taxid": taxid, "rank": rank, "count": count, "children": {}}
            previous[name] = new_entry
            previous = new_entry["children"]
            continue

        current["count"] += count
        previous = current["children"]
        previous_rank = rank

    return entries


def yield_entries(entries, total, indent=0):
    """Get entries in printable form."""
    for i, j in entries.items():
        perc = "{:.2%}".format(j["count"] / total)
        yield (indent, i, j["taxid"], j["count"], perc, j["rank"])
        for k in yield_entries(j["children"], total, indent + 1):
            yield k


def create_results_json(prefix, lineages, bracken, report):
    """Run lineage aggregation algorithm."""
    bracken_counts = {}
    entries = {}
    total = 0
    with open(bracken) as f:
        bracken = f.readlines()
    if len(bracken) > 0:
        for i in bracken:
            bracken_counts[i.split()[1]] = i.split()[0]
        with open(lineages) as f:
            infile = f.readlines()
        for line in infile:
            try:
                entries = update_or_create_count(line, entries, bracken_counts)
                total += 1
            except ValueError:
                sys.stderr.write(
                    """Lineage for tax id {} not found in taxonomy database""".format(
                        str(line)
                    )
                )
    with open(report) as f:
        report_file = f.readlines()
        for line in report_file:
            if line.split()[4] == "0" and "unclassified" in line:
                unclassified_count = line.split()[2]
                entries = update_or_create_unclassified(entries, unclassified_count)
                total += int(unclassified_count)
    output_report = open("{}.lineages.txt".format(prefix), "w")
    output_json = open("{}.lineages.json".format(prefix), "w")
    for entry in yield_entries(entries, total):
        [indent, name, taxid, count, perc, rank] = entry
        output_report.write(
            " ".join(
                ["-" * (indent + 1), name, str(taxid), str(count), perc, rank, "\n"]
            )
        )
    output_json.write(json.dumps(entries))
    print(output_json)
    return output_json
    
######

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


def isin_taxid_list(df:pd.DataFrame, list_taxid:list) -> pd.DataFrame:
    df_in = df[df.taxid.isin(list_taxid)]
    return df_in


def search_rank(df:pd.DataFrame, rank:["Species", "Genus", "Family", "Order", "Kingdom", "Phylum"]) -> pd.DataFrame:
    """take first letter of rank to search for (as seen in report results)."""
    #df_rank = df[df.rank.str.contains(rank[0], case=False, na=False)]
    print(df)
    print(rank)
    df_rank = df[df["rank"].eq(rank[0])]
    return df_rank
# may need to change ^ to .eq other .str.contains


def search_species(df:pd.DataFrame) -> pd.DataFrame:
    df_species = df[df.rank.str.contains("S", case=False, na=False)]
    return df_species


def is_virus(df:pd.DataFrame, database_path:str) -> pd.DataFrame:
    """initiate TaxaPlease and use isVirus function (->bool) to determine if taxids found are listed as viruses in NCBI database."""
    taxaPlease = TaxaPlease(database=database_path)
    df = df.assign(is_virus=df['taxid'].apply(lambda x: taxaPlease.isVirus(x)))
    if len(df) >=1:
        presence = True
    else: 
        presence = False
    return df, presence


def virus_presence(df:pd.DataFrame):  #, rank:str, run_id:str, climb_id:str):
    """check to see if there are any return viral reads based on the length of passed DataFrame."""
    if len(df) == 0:
        return False
    elif len(df) > 0:
        # df.to_csv(f"{run_id}_{climb_id}_{rank}_virus_presence.csv")
        return True


def get_kmer_matches(df_filtered_report:pd.DataFrame, df_results:pd.DataFrame, climb_id:str, run_id:str) -> pd.DataFrame:
    """for climb_id/run_id that return species level match(es) create dataframe of data where kmer matches for viral species
    occur. This is to be used in the info json."""
    list_taxid = list(df_filtered_report.taxid)
    # df_match = [lambda x: df_results.taxid.isin(x) for x in list_taxid]
    df_match = df_filtered_report[df_filtered_report["taxid"].isin(list_taxid)]
    return df_match


def create_json(run_id:str, climb_id:str, df_genus: pd.DataFrame, df_species: pd.DataFrame, genus_presence:bool, species_presence:bool): 
    json_setup = {
        "climb_id": climb_id,
        "run_id": run_id,
        "virus_presence_genus": genus_presence,
        "virus_presence_species": species_presence,
        "genus": ', '.join(df_genus["name"].str.strip()),
        "genus_taxids": ', '.join(df_genus["taxid"].astype(str)),
        "species": ', '.join(df_species["name"].str.strip()),
        "species_taxids": ', '.join(df_species["taxid"].astype(str)),
        # "kmer_matches": list[df_virus_kmer_matches["kmer_map"]]
    }
    print(json_setup)
    # json_file = json.dump(json_setup)
    with open('data.json', 'w') as f:
        json.dump(json_setup, f)
    return json_setup


def create_analysis_fields(
    record_id: str, qc_thresholds: dict, headline_result: str, reclassification_results : dict, server: str
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
        analysis_name="ukhsa-classifier-qc-metrics",
        analysis_description="This is an analysis to generate QC statistics for individual samples",
    )
    onyx_analysis.add_package_metadata(package_name="mscape-sample-qc")
    methods_fail = onyx_analysis.add_methods(methods_dict=qc_thresholds)
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
    print(args.database)
    df = load_report(in_path=args.report)
    print(df)
    df_virus = is_virus(df, args.database)
    print(df_virus)
    df_virus_genus = search_rank(df=df_virus,
                                 rank="Genus")
    
    df_virus_species = search_rank(df=df_virus,
                                   rank="Species")
    
    df_virus_species = is_virus(df_virus_species, args.database)
    
    #results_dict = create_results_json(prefix=args.runid, 
    #                                   lineages=args.lineages, 
    #                                   bracken=args.bracken,
    #                                   report=args.report)
    
    #json = create_json(run_id=args.runid, 
    #                   climb_id=args.climbid, 
    #                   df_genus=df_virus_genus, 
    #                   df_species=df_virus_species, 
    #                   genus_presence=virus_presence(df_virus_genus), 
    #                   species_presence=virus_presence(df_virus_species))
    
    analysis_fields_dict = create_analysis_fields(record_id=args.climbid,
                                                  qc_thresholds="", 
                                                  headline_result=str(virus_presence(df_virus_genus)), 
                                                  # reclassification_results=results_dict, 
                                                  reclassification_results=args.json,
                                                  server="")
    
    write_onxy_results_to_json(results_dict=analysis_fields_dict,
                               climb_id=args.climbid,
                               results_dir=os.getcwd())
    