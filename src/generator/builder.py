import logging
from typing import Dict, Any, List
from .models import ScenarioPrototype, ScenarioEvent, ParameterRange
from .template_manager import TemplateManager
from .parameterizer import SymbolicParameterizer

logger = logging.getLogger(__name__)

class PrototypeBuilder:
    """
    The orchestrator for Prototype Generation.
    Takes LLM analysis outputs and generates the formal search space blueprint.
    """
    
    def __init__(self):
        self.template_manager = TemplateManager()
        self.parameterizer = SymbolicParameterizer()
        
    def build_prototype(self, llm_analysis_result: Dict[str, Any]) -> ScenarioPrototype:
        """
        Executes the 3-stage generation process described in Section 3.3.
        """
        logger.info("Initializing Scenario Prototype Generation...")
        
        cause_chain = llm_analysis_result.get("cause_chain", "")
        context = llm_analysis_result.get("contextual_reasoning", "")
        fixed_points = llm_analysis_result.get("fixed_points", [])
        
        # Stage 1: Template Selection
        base_env = self.template_manager.select_template(cause_chain, fixed_points)
        base_env["weather"] = "rain" if "wet" in context.lower() else "clear"
        
        # Stage 2: Symbolic Parameterization (Define Search Space)
        # Mocking specific LLM numeric inferences for the demo
        mock_llm_numbers = {"ego_speed_estimate": 25.0, "npc_cutin_speed": 28.0}
        participants = self.parameterizer.build_participants(mock_llm_numbers)
        
        # Stage 3: Event Sequencing
        events = [
            ScenarioEvent(
                participant_id="NPC_CutIn",
                action_type="AggressiveLaneChange",
                trigger_condition="SimulationTime > 3.0",
                action_parameters=[
                    ParameterRange("duration", 1.0, 3.0) # Fuzzer will find the most dangerous duration
                ]
            )
        ]
        
        # Encapsulate into the final Prototype blueprint
        prototype = ScenarioPrototype(
            name="Generated_Fixed_Point_Guided_Prototype",
            environment_context=base_env,
            participants=participants,
            event_sequence=events,
            targeted_fixed_points=fixed_points # Embedded as Oracles for NSGA-II
        )
        
        logger.info(f"Prototype successfully built with {len(participants)} participants and {len(fixed_points)} target oracles.")
        return prototype
