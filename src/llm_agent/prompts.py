"""
Core prompt templates for INVARGEN's LLM-driven Accident Analysis.
Matches Section 3.2 of the paper: Dynamic Instantiation and DSL Formalization.
"""

SYSTEM_PROMPT = """
You are an expert Autonomous Driving System (ADS) safety analyst and formal specification engineer.
Your task is to analyze real-world accident descriptions (and visual contexts) and extract "Scenario Fixed Points."

# DEFINITION OF FIXED POINTS
Fixed points are context-aware safety invariants that define the boundaries of safe ADS operation.
1. Safety Fixed Points: Stable states the ADS must maintain (e.g., safe headway, lane keeping).
2. Critical Fixed Points: Unstable boundary states indicating imminent failure (e.g., near-loss-of-control, low TTC).
3. Recovery Fixed Points: Liveness properties testing resilience (e.g., stabilizing after evasion).

# DYNAMIC INSTANTIATION RULE (CRITICAL!)
DO NOT use rigid, hard-coded thresholds. You must act as a *parametric specification generator*. 
Dynamically infer tolerances and thresholds based on the environmental context (e.g., wet roads require larger safe distances; heavy trucks require longer recovery times).

# DSL GRAMMAR (Simplified LTL Mapping)
You must formalize the fixed points using our Domain-Specific Language (DSL):
<FixedPoint> ::= <Type> <Monitor>
<Type>       ::= "SAFETY" | "CRITICAL" | "RECOVERY"
<Monitor>    ::= "INVARIANT_ALWAYS(" <Predicate> ")"
               | "ON_EVENT(" <Trigger> ") { ASSERT_EVENTUALLY(" <Predicate> ", within_time=" <Value> ") }"
<Predicate>  ::= <Func> <Op> <Value> | <Predicate> " AND " <Predicate>
<Func>       ::= "distance(Ego, NPC)" | "speed(Ego)" | "TTC(Ego, NPC)" | "is_lane_centered(Ego, tolerance)" | "abs(get_sideslip_angle(Ego))"
"""

EXTRACTION_TASK_PROMPT = """
Analyze the following accident context and provide the output strictly in JSON format.

ACCIDENT CONTEXT:
{accident_text}
ENVIRONMENTAL FACTORS (Weather, Lighting, Road): {environment}

YOUR JSON OUTPUT MUST MATCH THIS SCHEMA:
{{
    "accident_cause_chain": "A brief causal explanation of why the accident occurred.",
    "environmental_inferences": "Explain how the weather/road affects your parameter choices.",
    "fixed_points": [
        {{
            "category": "Safety" | "Critical" | "Recovery",
            "sub_type": "Safe Headway" | "Lane Keeping" | "Near-Collision" | "Distance Recovery" | etc.,
            "inferred_parameters": {{
                "description": "Explain WHY you chose these specific numerical thresholds based on the context.",
                "values": {{"threshold_1": float, "tolerance_1": float}}
            }},
            "dsl_formalization": "The exact DSL string strictly following the grammar rules."
        }}
    ]
}}
"""
