"""
Data models for Scenario Prototypes.
Matches Section 3.3: Symbolic Parameterization and Search Space Definition.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple

@dataclass
class ParameterRange:
    """Represents a searchable symbolic range rather than a static constant."""
    name: str
    min_val: float
    max_val: float
    distribution: str = "uniform"  # Can be mutated by LLM (e.g., normal, lognormal)

@dataclass
class Participant:
    """Traffic participant with parameterized initial states."""
    id: str
    role: str  # "Ego", "NPC", "Pedestrian"
    vehicle_type: str
    initial_lane: int
    longitudinal_offset_range: ParameterRange
    speed_range: ParameterRange

@dataclass
class ScenarioEvent:
    """Represents high-level event sequences (Stage 3 in Sec 3.3)."""
    participant_id: str
    action_type: str  # e.g., "AggressiveLaneChange", "EmergencyBraking"
    trigger_condition: str  # e.g., "TTC < 2.0"
    action_parameters: List[ParameterRange]

@dataclass
class ScenarioPrototype:
    """
    The abstract blueprint defining the search space for the MOEA (NSGA-II).
    Embeds Fixed Points directly as test oracles.
    """
    name: str
    environment_context: Dict[str, Any]
    participants: List[Participant]
    event_sequence: List[ScenarioEvent]
    # Fixed Points encapsulated as explicit optimization targets (Test Oracles)
    targeted_fixed_points: List[Any]
