#!/usr/bin/env nextflow


process UN {
    container 'quay.io/biocontainers/kraken2:2.17--pl5321h077b44d_0'
    cpus = 4
    memory = '16GB'

    script:
    """
    pwd
    kraken2 --db /shared/team/reference_databases/kraken/curated-viral-db/2025-10-01_taxonomy_2023_10_01/ s3://mscape-published-read-fractions/C-E745C4D928/C-E745C4D928.human_filtered.fastq.gz --output /shared/team/mike/projects/virus_reclassification/test_results.txt --report /shared/team/mike/projects/virus_reclassification/test_report
    """
}
