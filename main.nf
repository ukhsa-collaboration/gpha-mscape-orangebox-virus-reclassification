#!/usr/bin/env nextflow

include { KRAKEN } from './modules/run_custom_kraken.nf'
include { UN } from './modules/un.nf'
include { ANALYSIS } from './modules/run_kraken_analysis.nf'

params.csv = ""
params.fastq = '/shared/team/ashley/unclassifier-controls/kraken_on_viral/reads/C-18A1E8AC40.viral.fastq.gz'  // original fastq input 
params.database = '/shared/team/reference_databases/kraken/curated-viral-db/2025-10-01/' // path to AK's custom Kraken Database
params.output = "/results"

workflow {
    //fasta_ch = Channel.of(params.fastq)  // need to activate this bad boy - channel per fastq
    //output_ch = Channel.of(params.output) // activate ?
    // UN() // test with harcoded link
    KRAKEN(params.fastq, params.database test_climbid, test_runid)
    ANALYSIS(KRAKEN.out.report, KRAKEN.out.results, params.output)

}



// TODO: move custom DB -> s3 bucket 