# 🧬 Hybrid Evolutionary Search Engine (NSGA-II + Fuzzing)

> **Reference:** Section 3.4 & Algorithm 1 in the INVARGEN paper.

This module implements the **Fixed-Point Guided Hybrid Search Algorithm**. It acts as the optimization core of INVARGEN, systematically exploring the parameter space defined by the scenario prototypes to discover deep ADS vulnerabilities.

## 🚀 Algorithm Overview

Unlike traditional Search-Based Software Testing (SBST) that relies on random mutations, our engine synergizes two distinct operators within a Multi-Objective Evolutionary Algorithm (MOEA) framework:

1. **Local Exploitation (Intelligent Fuzzing):** Guided by the LLM's fixed-point sensitivity analysis, the fuzzer calculates pseudo-gradients to aggressively perturb continuous parameters (e.g., speed, braking timing) to push the ADS over the safety boundary.
2. **Global Exploration (Structural Mutation):** When population diversity stalls (measured by crowding distance), the engine delegates mutation to the LLM to introduce qualitative semantic shifts (e.g., changing weather to rain, changing an NPC from a sedan to a truck), effectively escaping local optima.

## 🎯 Multi-Objective Fitness (Eq. 1-4)
The engine optimizes a 4-dimensional objective vector $J(S)$ for each scenario $S$:
* $J_{safety}$: Maximizes the depth and duration of Safety Fixed Point violations.
* $J_{recovery}$: Maximizes the time required to regain stability (Recovery Failure).
* $J_{crit}$: Maximizes the criticality (minimizing Time-To-Collision).
* $J_{div}$: Maximizes semantic and parameter diversity to prevent mode collapse.

## 🚀 Algorithm Details



## 📂 Module Structure
* `fitness.py`: Implements the objective function calculations based on simulation traces.
* `operators.py`: Contains the `IntelligentFuzzer` and `StructuralMutator` logic.
* `nsga2.py`: The main orchestrator implementing the Non-dominated Sorting and generation loops (Algorithm 1).
