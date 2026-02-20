import logging
from .models import ParameterRange, Participant, ScenarioEvent

logger = logging.getLogger(__name__)

class SymbolicParameterizer:
    """
    Handles Stage 2: Symbolic Parameterization and Search Space Definition.
    Converts concrete accident inferences into bounded searchable ranges.
    """
    
    @staticmethod
    def infer_speed_range(inferred_speed: float, context: str) -> ParameterRange:
        """Dynamically creates a search bound around the LLM inferred speed."""
        # e.g., allow fuzzer to explore +/- 20% of the inferred speed
        variance = 0.20
        # If the context is 'wet' or 'fog', we might shift the distribution
        if "wet" in context.lower():
            variance = 0.30  # Wider range to explore slipping dynamics
            
        min_s = round(inferred_speed * (1 - variance), 1)
        max_s = round(inferred_speed * (1 + variance), 1)
        return ParameterRange(name="speed", min_val=min_s, max_val=max_s)

    @staticmethod
    def build_participants(llm_inferences: dict) -> list:
        """
        Translates LLM's static actor descriptions into Parameterized Participants.
        """
        participants = []
        
        # Ego Vehicle (Base State)
        ego_speed = llm_inferences.get("ego_speed_estimate", 20.0)
        ego = Participant(
            id="Ego",
            role="EgoVehicle",
            vehicle_type="Car",
            initial_lane=1,
            longitudinal_offset_range=ParameterRange("offset", 0.0, 0.0), # Ego is reference
            speed_range=SymbolicParameterizer.infer_speed_range(ego_speed, "normal")
        )
        participants.append(ego)
        
        # NPC Generation based on context (e.g., the Cut-in vehicle)
        if "npc_cutin_speed" in llm_inferences:
            npc_speed = llm_inferences["npc_cutin_speed"]
            npc = Participant(
                id="NPC_CutIn",
                role="NPCVehicle",
                vehicle_type="Car",
                initial_lane=2,
                longitudinal_offset_range=ParameterRange("offset", 10.0, 30.0), # Fuzzer explores gap
                speed_range=SymbolicParameterizer.infer_speed_range(npc_speed, "aggressive")
            )
            participants.append(npc)
            
        return participants
