#!/usr/bin/env nextflow


process ANALYSIS {
    container 'community.wave.seqera.io/library/biopython_taxonkit:f509bdb54ad22eed'
    publishDir "results", mode: 'copy'
    
    input:
        val climbid
        val runid
        path kraken_report
        path kraken_results
        val db_path

    output:
        // file "data.json"
        file "${climbid}_taxacounts.txt"
        file "${climbid}_taxa.txt"
        file "${climbid}_lineages.txt"
        file "${climbid}_viral_reclassifier.kraken.json"

    
    script:
    """
    cat "${kraken_report}" | cut -f5,3 | tail -n+3 > "${climbid}_taxacounts.txt"
    cat "${kraken_report}" | cut -f5 | tail -n+3 > "${climbid}_taxa.txt"
    taxonkit lineage --data-dir "${db_path}" -R "${climbid}_taxa.txt"  > "${climbid}_lineages.txt"
    aggregate_lineages_bracken.py -i "${climbid}_lineages.txt" -b "${climbid}_taxacounts.txt" -u "${kraken_report}" -p "temp_kraken"
    file1=`cat *.json`
    echo "{"'"${climbid}"'": "\$file1"}" >> "${climbid}_viral_reclassifier.kraken.json"
    """

    

}