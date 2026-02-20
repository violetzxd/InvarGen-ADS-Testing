# 📜 DSL & Template Library

> **Reference:** Section 3.2 & Section 3.3 in the INVARGEN paper.

This directory contains the foundational definitions for the INVARGEN framework:
1. **DSL Grammar (`dsl_grammar.bnf`):** The formal Backus-Naur Form (BNF) definition of our Domain-Specific Language, mapping natural language semantics to Linear Temporal Logic (LTL) for the optimization engine.
2. **Fixed Point Library (`fixed_points_lib.yaml`):** The semantic skeleton of Safety, Critical, and Recovery invariants. Note that thresholds here are *symbolic*—they are dynamically inferred by the LLM during runtime based on environmental context.
3. **Scenario Archetypes (`scenario_archetypes.yaml`):** The topological base maps used in Stage 1 of Prototype Generation.
