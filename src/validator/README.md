# 🛡️ Validator & Compiler Module

> **Reference:** Section 3.5 & RQ4 in the INVARGEN paper.

This module acts as the gatekeeper before any scenario is dispatched to the heavy 3D simulator (Carla/Panosim). It ensures that the evolutionary search engine does not exploit "physics glitches" to generate invalid violations (e.g., flying cars or infinite acceleration).

## ⚙️ Core Components

1. **Kinematic Checker (`kinematic_checker.py`):** Enforces physical plausibility by validating that the parameterized maneuvers (e.g., aggressive cut-ins) do not exceed real-world vehicle dynamic limits (Maximum Acceleration, Braking Deceleration, and Lateral Jerk). This addresses the "Construct Validity" of our testing framework.
   
2. **OpenSCENARIO Compiler (`osc_compiler.py`):**
   Serializes the validated INVARGEN internal DSL and Scenario Prototypes into industry-standard **OpenSCENARIO 1.x (.xosc)** format, linking them to appropriate OpenDRIVE (.xodr) road networks.
