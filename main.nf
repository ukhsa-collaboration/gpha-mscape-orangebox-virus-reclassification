#!/usr/bin/env nextflow

include { KRAKEN } from './modules/run_custom_kraken.nf'
include { UN } from './modules/un.nf'
include { ANALYSIS } from './modules/run_kraken_analysis.nf'



workflow {
     // Handle either samplesheet or climb id
     KRAKEN(params.arg_fastq, params.arg_kraken_database test_climbid, test_runid)
}