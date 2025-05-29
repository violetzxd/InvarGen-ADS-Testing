# InvarGen

This repository contains the artifact and code for the ASE 2025 submission:  
**"InvarGen: Fixed-Point Guided Scenario Generation via Multi-Modal LLM Reasoning and Software Testing Techniques"**.

---

## 🧠 Overview

InvarGen introduces a **symbolic scenario testing framework** to assess Autonomous Driving Systems (ADS) using realistic, variant-rich accident-inspired scenarios. Instead of generating scenarios blindly or relying solely on expert heuristics, InvarGen integrates:

- **Large Language Models (LLMs)** for accident analysis and root cause summarization
- **Symbolic fixed point reasoning** to guide scenario prototyping
- **Software Engineering (SE)–driven variation techniques** to explore behavioral edges
- **Formal realism assurance** to ensure scenario plausibility and test value

The entire pipeline enables automatic generation, mutation, and validation of test scenarios with symbolic safety or liveness invariants embedded.

---

## 🛠 Core Modules

### 1️⃣ `llm_analysis/`: LLM-Driven Accident Analysis & Fixed Point Identification

- Uses GPT-like models to summarize accident logs, identify causal chains, and detect *behavioral fixed points* (e.g., late merge, aggressive lane change).
- Outputs abstract representations of conflict triggers and scenario anchors.

**Inputs**: Natural language accident reports or trajectory logs  
**Outputs**: Symbolic fixed point schema (e.g., JSON or logical templates)

---

### 2️⃣ `prototype_generation/`: Fixed Point-Guided Scenario Prototyping

- Builds base scenarios using symbolic anchors (e.g., ego near intersection with slow mover ahead).
- Uses OSM or manually defined topology + actor intents to reconstruct minimal conflict conditions.

**Inputs**: Fixed points, road topology  
**Outputs**: Scenario prototype in OpenSCENARIO or PanoSim-compatible JSON

---

### 3️⃣ `scenario_fuzzing/`: SE Method–Driven Scenario Variation & Fuzzing

- Applies SE principles (e.g., boundary testing, combinatorial testing, parameter sweep) to inject meaningful variance:
  - Speed perturbation
  - Starting location shifts
  - Additional traffic agents
- Inspired by software fuzzing but adapted to continuous simulation dynamics.

**Outputs**: Scenario variants to explore edge behavior and robustness.

---

### 4️⃣ `realism_assurance/`: Scenario Formalization & Realism Validation

- Ensures generated scenarios adhere to road rules and real-world realism constraints.
- Uses domain rules and constraint solvers (e.g., Z3) to validate:
  - Temporal causality
  - Plausible actor behavior
  - Realistic trajectory patterns

**Outputs**: Pass/fail flags or realism scores + violation logs.

## 📈 Evaluation

- To evaluate InvarGen, we used diverse real-world datasets, including UCF-Crime, CADP, and a curated Online Fusion Dataset—covering various traffic scenarios and accident types.
- The target ADS was deployed on representative platforms (e.g., Apollo, Autoware) within high-fidelity simulators such as Carla, LGSVL, and Panosim.
- We employed cutting-edge multi-modal LLMs (e.g., GPT-4o, Gemini Pro Vision, LLaVA, CogVLM) with tailored API configurations and prompts.
- InvarGen was compared against baselines including AutoSceneGen, LeGEND, SimADFuzz, and AmbieGen, representing both LLM-based and traditional SE methods.
- All tests used equal compute and simulation budgets. Fixed-point effectiveness was quantitatively assessed via ADS state thresholds, trajectory deviation, and control smoothness.

---

