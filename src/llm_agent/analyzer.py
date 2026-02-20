import json
import logging
from typing import Dict, Any
from .llm_client import LLMClient
from .prompts import SYSTEM_PROMPT, EXTRACTION_TASK_PROMPT
from .fixed_point_parser import parse_fixed_points

logger = logging.getLogger(__name__)

class AccidentAnalyzer:
    """
    The orchestrator for LLM-driven accident analysis.
    Corresponds to 'LLM-Driven Accident Analysis and Fixed Point Identification' (Fig 2).
    """
    
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm_client = LLMClient(model_name=model_name)
        
    def analyze_accident(self, accident_report: str, env_context: str) -> Dict[str, Any]:
        """
        Extracts Fixed Points from an accident report.
        """
        logger.info("Starting LLM analysis for fixed point extraction...")
        
        # Format the prompt with the specific accident context
        user_prompt = EXTRACTION_TASK_PROMPT.format(
            accident_text=accident_report,
            environment=env_context
        )
        
        # Call the LLM (temperature set to 0.2 for analytical consistency)
        raw_response = self.llm_client.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.2,
            response_format="json_object"
        )
        
        try:
            analysis_result = json.loads(raw_response)
            
            # Parse the raw JSON into structured Python objects for the Fuzzing module
            structured_fps = parse_fixed_points(analysis_result.get("fixed_points", []))
            
            logger.info(f"Successfully extracted {len(structured_fps)} Fixed Points.")
            return {
                "cause_chain": analysis_result.get("accident_cause_chain"),
                "contextual_reasoning": analysis_result.get("environmental_inferences"),
                "fixed_points": structured_fps
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode LLM response: {e}")
            raise
