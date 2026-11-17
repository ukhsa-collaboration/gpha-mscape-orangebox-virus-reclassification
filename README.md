
# <img src="assests/UKHSA_Logo.png" width="75" height="75"> GPHA mSCAPE OrangeBox Kraken Reclassification (K^2)

---

## Table of Contents

- [ GPHA mSCAPE OrangeBox Kraken Reclassification (K^2)](#-gpha-mscape-orangebox-kraken-reclassification-k2)
  - [Table of Contents](#table-of-contents)
  - [Info](#info)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Install](#install)
  - [Usage](#usage)
  - [To run the pipeline](#to-run-the-pipeline)
  - [Commands](#commands)
  - [Troubleshooting](#troubleshooting)
  - [Change-log](#change-log)
  - [To-do](#to-do)

---

## Info

| Name         | GPHA mSCAPE OrangeBox Virus Reclassification                                        |
|--------------|-------------------------------------------------------------------------------------|
| Version      | 2.0.1                                                                               |
| Last Updated | 17.10.2027                                                                          |
| Author(s)    | GPHA                                                                                |
| Summary      | NextFlow data pipeline for mSCAPE rerunning of Kraken with custom database and producing results|

---

## Features

---

## Requirements

> [!Warning]

---

## Install

- Start a terminal session
- Navigate to desired parent directory
- Run:

```bash
git clone https://github.com/ukhsa-collaboration/gpha-mscape-orangebox-virus-reclassification.git

```

> [!Tip]
> It is reccomended to run in screen or TMUX session in case of crash
---

## Usage

## To run the pipeline

```bash
cd gpha-mscape-orangebox-virus-reclassification
nextflow run main.nf 
```

---

## Commands
>
> [!Note]
> Arguments can be filled out in the config/params.config file

- --fastq - path to fastq files
- --kraken_database - path to custom Kraken database folder
- --output - output directory path
- --runid - Run ID
- --tp_db_path - path to folder containing TaxaPlease database
- --db_path - path to folder containing taxa database files

---

## Troubleshooting

> [!Important]
> Make sure all paths are entered correctly <br>
> Make sure necessary DB files are within directed folders
---

## Change-log

---

## To-do

- [ ] \(Optional) run ruff linter on .py files
- [ ] \(Optional) task

---
