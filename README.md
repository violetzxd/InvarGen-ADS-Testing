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

## 🌟 Main Contributions

This repository implements the core innovations presented in our paper, specifically designed to address the "curse of dimensionality" and the "oracle problem" in ADS scenario generation:

* **Novel Framework Paradigm:** We propose INVARGEN, the first framework to utilize multi-modal LLMs as *active parametric specification generators* rather than passive scene translators. It seamlessly bridges semantic accident analysis with systematic software testing.
* **Dynamic Semantic Abstraction:** We introduce the concept of **Scenario Fixed Points**—context-aware safety invariants (e.g., adaptive safe headway thresholds) that are dynamically instantiated from unstructured accident videos. These adapt flexibly to environmental contexts (like weather or road friction) to provide precise guidance for robustness testing.
* **Hybrid Evolutionary Mechanism:** We implemented a Fixed-Point Guided Hybrid Search algorithm. It synergizes two distinct operators: *Intelligent Fuzzing* for the local exploitation of boundary parameters, and *LLM-Driven Structural Mutation* for the global exploration of diverse environmental contexts.
* **Rigorous Empirical Validation:** Through extensive evaluation involving 30 independent runs over 1,400 synthesized scenarios, INVARGEN statistically outperforms state-of-the-art baselines. It achieves a 30% fixed-point violation rate, discovers 37.5% more unique violation types, and maintains 100% compatibility with OpenX standards.

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

