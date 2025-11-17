
# <img src="https://upload.wikimedia.org/wikipedia/fi/6/69/UKHSA_Logo.svg.png" width="75" height="75"> GPHA mSCAPE OrangeBox Virus Reclassification
---

## Table of Contents

- [Info](#info)
- [Features](#features)
- [Requirements](#requirements)
- [Install](#install)
- [Usage](#usage)
- [Commands](#commands)
- [Troubleshooting](#troubleshooting)
- [Change-log](#change-log)
- [To-do](#to-do)
---

## Info

| Name         | GPHA mSCAPE OrangeBox Virus Reclassification                                        |
|--------------|-------------------------------------------------------------------------------------|
| Version      | 0.1                                                                                 |
| Last Updated | 17.11.2025                                                                          |
| Author(s)    | Mike Brown                                                                          |
| Contact      | michael.d.brown@ukhsa.gov.uk                                                        |
| Summary      | NextFlow data pipleine for rerunning Kraken with comprehensive custom viral database|

---

## Features

<img width="1051" height="700" alt="image" src="https://github.com/user-attachments/assets/db9a08d0-a8e4-4ccf-8476-8d0d6c160289" />

---

## Requirements
> [!Warning]
> To run it is neccessary to have obtained:
> Access to BRYN <br>
---

## Install
- Login to BRYN
- Start notebook server
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
##### To run the pipeline
  - Navigate to gpha-mscape-orangebox-virus-reclassification folder
  - Run the NextFlow data pipeline
  - Run:
```bash
cd gpha-mscape-orangebox-virus-reclassification
nextflow run main.nf 
```
---

## Commands
> [!Note]
> --output-dir
> --input-dir
---

## Troubleshooting

> [!Important]
> Make sure all paths are entered correctly <br>
---

## Change-log

---

## To-do

- [x] move related lineage grouping files into current repo
- [x] restructure repo to follow of GPHA standards
- [x] reformat auto_linelist.py and move away from stdout calls
- [ ] \(Optional) convert lineage_line_groups_linkage.ipynb notebook -> script
- [ ] \(Optional) task

---
