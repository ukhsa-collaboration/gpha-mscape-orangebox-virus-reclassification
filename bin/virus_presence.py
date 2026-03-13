#!/usr/bin/env python3

import pandas as pd
import sys
import os
import argparse
from pathlib import Path
from taxaplease.taxaplease import TaxaPlease
import json



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
    df_rank = df[df["rank"].eq(rank[0])]
    return df_rank
# may need to change ^ to .eq other .str.contains


def search_species(df:pd.DataFrame) -> pd.DataFrame:
    df_species = df[df.rank.str.contains("S", case=False, na=False)]
    return df_species


def search_genus(df:pd.DataFrame) -> pd.DataFrame:
    df_species = df[df.rank.str.contains("G", case=False, na=False)]
    return df_species


def is_virus(df:pd.DataFrame, database_path:str) -> pd.DataFrame:
    """initiate TaxaPlease and use isVirus function (->bool) to determine if taxids found are listed as viruses in NCBI database."""
    taxaPlease = TaxaPlease(database=database_path)
    df = df.assign(is_virus=df['taxid'].apply(lambda x: taxaPlease.isVirus(x)))
    return df


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
        "virus_presence_genus": virus_presence(genus_presence),
        "virus_presence_species": virus_presence(species_presence),
        "genus": ', '.join(df_genus["name"].str.strip()),
        "genus_taxids": ', '.join(df_genus["taxid"].astype(str)),
        "species": ', '.join(df_species["name"].str.strip()),
        "species_taxids": ', '.join(df_species["taxid"].astype(str)),
        # "kmer_matches": list[df_virus_kmer_matches["kmer_map"]]
    }
    # print(json_setup)
    # json_file = json.dump(json_setup)
    print(genus_presence)
    with open(f'{climb_id}_data.json', 'w') as f:
        json.dump(json_setup, f)
    return json_setup


if __name__ == "__main__":
    """a main function"""
    parser = argparse.ArgumentParser(description="yes.")
    parser.add_argument('--report', type=str, required=True, help="path to Kraken report file")
    parser.add_argument('--results', type=str, required=True, help="path to Kraken results file")
    parser.add_argument('--climbid', type=str, required=False, help="climb id")
    parser.add_argument('--runid', type=str, required='--climb-id' in sys.argv, help="run id")
    parser.add_argument('--outdir', type=str, required=False, help="output directory path")
    parser.add_argument('--database', type=str, required=True, help='input databse path')
    
    args = parser.parse_args()
    df = load_report(in_path=args.report)
    df_virus = is_virus(df, args.database)
    df_virus_genus = search_rank(df=df_virus,
                                 rank="Genus")
    df_virus_presence_genus = is_virus(df_virus_genus, args.database)
    df_virus_species = search_rank(df=df_virus,
                                   rank="Species")
    df_virus_presence_species = is_virus(df_virus_species, args.database)
    create_json(run_id=args.runid, 
                climb_id=args.climbid,
                df_genus=df_virus_genus, 
                df_species=df_virus_species, 
                genus_presence=df_virus_presence_genus, 
                species_presence=df_virus_presence_species)
    