#!/usr/bin/env nextflow

include { KRAKEN } from './modules/run_custom_kraken.nf'
include { ANALYSIS } from './modules/run_kraken_analysis.nf'


workflow {
     fasta = channel.fromPath(params.fastq)
     KRAKEN(fasta, params.kraken_database, params.runid)
     ANALYSIS(KRAKEN.out.climbid, params.runid, KRAKEN.out.kreport, KRAKEN.out.kresults, params.db_path)
}