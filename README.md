# INVARGEN: Fixed-Point Guided ADS Scenario Generation

[![Anonymous Submission](https://img.shields.io/badge/ISSTA-2026-blue)](https://conf.researchr.org/home/issta-2026)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> **Note to Reviewers:** This repository contains the **replication package** for the paper *"Fixed-Point Guided ADS Scenario Generation via Multi-Modal LLM Reasoning and Software Testing"*. To maintain anonymity, all author information and institutional links have been redacted.

## 📖 Overview

**INVARGEN** is a novel framework that bridges semantic accident analysis and systematic software testing. It utilizes Multi-Modal LLMs to extract **"Scenario Fixed Points"** (safety invariants) from real-world accident data, which then guide a hybrid evolutionary search (Intelligent Fuzzing + Structural Mutation) to generate robust, critical, and executable test scenarios for Autonomous Driving Systems (ADS).

### Key Features
* **LLM-Driven Specification:** Automatically extracts *Safety*, *Critical*, and *Recovery* fixed points from videos/images.
* **Hybrid Evolutionary Search:** Combines global exploration (NSGA-II) with local exploitation (Gradient-based Fuzzing).
* **Industry Standard Output:** Generates scenarios compatible with **OpenSCENARIO 1.x**, **OpenDRIVE**, and **ASAM OSI**.
* **Multi-Simulator Support:** Validated on **Carla** and **Panosim**.

---

## 📂 Repository Structure

The project is structured to mirror the pipeline described in **Section 3** of the paper:

```text
INVARGEN_Replication/
├── data/
│   ├── accident_samples/       # (RQ1) Representative subset of UCF-Crime/CADP (Input)
│   └── dsl_templates/          # Pre-defined scenario archetypes and DSL grammar
├── src/
│   ├── llm_agent/              # (Sec 3.2) Modules for Fixed Point Extraction (GPT-4o/Gemini)
│   ├── generator/              # (Sec 3.3) Prototype Generation & Serialization
│   ├── search_engine/          # (Sec 3.4) Hybrid Evolutionary Search (NSGA-II + Fuzzing)
│   └── validator/              # (Sec 3.5) Kinematic checks & OpenSCENARIO compilation
├── experiments/                # Scripts to reproduce RQ2-RQ5
│   ├── rq2_search_effectiveness/
│   ├── rq3_defect_discovery/
│   ├── rq4_validity/
│   └── rq5_ablation/
├── outputs/                    # Generated .xosc and .xodr files
├── requirements.txt            # Python dependencies
└── run_demo.py                 # One-click demo script

