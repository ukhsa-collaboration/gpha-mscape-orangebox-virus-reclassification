#!/usr/bin/env nextflow

include { KRAKEN } from './modules/run_custom_kraken.nf'
include { UN } from './modules/un.nf'
include { ANALYSIS } from './modules/run_kraken_analysis.nf'



workflow {
     // KRAKEN(params.arg_fastq, params.arg_kraken_database, params.test_climbid, params.test_runid)
     ANALYSIS(params.test_climbid, params.test_runid, params.test_kraken_report, params.test_kraken_results, "test", params.db_path)
}