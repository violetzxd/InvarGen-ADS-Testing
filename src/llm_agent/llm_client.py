import os
import openai
import logging

logger = logging.getLogger(__name__)

class LLMClient:
    """
    A lightweight wrapper for LLM API calls.
    Supports OpenAI API for replicating the GPT-4o experiments in the paper.
    """
    def __init__(self, model_name: str = "gpt-4o"):
        self.model_name = model_name
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            logger.warning("OPENAI_API_KEY is not set. Using mock mode for peer review demo.")
            self.client = None
        else:
            self.client = openai.OpenAI(api_key=self.api_key)

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.2, response_format: str = "text") -> str:
        """Sends the request to the LLM."""
        
        # MOCK MODE: If reviewers run the code without an API key, return a pre-computed response.
        if not self.client:
            return self._get_mock_response()
            
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            response_format={"type": response_format} if response_format == "json_object" else None
        )
        
        return response.choices[0].message.content

    def _get_mock_response(self) -> str:
        """Returns a cached response for the peer-review demo (e.g., the Cut-in scenario)."""
        return """
        {
            "accident_cause_chain": "Aggressive cut-in by NPC forcing Ego to emergency brake on a wet surface.",
            "environmental_inferences": "Wet road friction is low; braking distance must be dynamically increased from standard 10m to 15m.",
            "fixed_points": [
                {
                    "category": "Safety",
                    "sub_type": "Safe Headway",
                    "inferred_parameters": {
                        "description": "Standard headway is 10m, added 5m buffer due to wet road constraint.",
                        "values": {"min_safe_distance": 15.0}
                    },
                    "dsl_formalization": "INVARIANT_ALWAYS(distance(Ego, NPC_CutIn) > 15.0)"
                },
                {
                    "category": "Recovery",
                    "sub_type": "Safe Distance Recovery",
                    "inferred_parameters": {
                        "description": "Due to wet conditions, ADS needs more time to restabilize speed.",
                        "values": {"within_time": 8.0}
                    },
                    "dsl_formalization": "ON_EVENT(emergency_braking_start(Ego)) { ASSERT_EVENTUALLY(distance(Ego, NPC_Front) > 15.0, within_time=8.0) }"
                }
            ]
        }
        """
