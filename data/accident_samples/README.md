# 🗂️ Accident Samples (Peer-Review Subset)

> **Reference:** Section 3.1 & RQ1 in the INVARGEN paper.

Due to the file size limits of the anonymous repository and the copyright restrictions of the full UCF-Crime and CADP datasets, this directory contains a **representative subset of 20 accident cases** used to demonstrate the INVARGEN pipeline and reproduce **RQ1 (Semantic Extraction Accuracy)**.

## Directory Structure per Case
Each accident case folder (e.g., `case_001_cut_in/`) contains:
1. `report.txt`: The textual accident description (police report or natural language summary).
2. `frames/`: Representative keyframes extracted from the accident dashcam video (simulating the multi-modal input).
3. `ground_truth.json`: The human-annotated "Scenario Fixed Points" used as the baseline to evaluate the LLM's extraction accuracy in RQ1.
