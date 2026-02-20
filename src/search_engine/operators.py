"""
Hybrid Search Operators.
Contains the Local Exploitation (Fuzzing) and Global Exploration (Mutation) operators.
"""
import random
import copy
import logging

logger = logging.getLogger(__name__)

class IntelligentFuzzer:
    """
    Handles Local Exploitation.
    Perturbs numeric parameters around the Fixed Point boundaries.
    """
    def __init__(self, step_size: float = 0.1):
        self.step_size = step_size

    def fuzz(self, scenario_prototype: dict, target_fp: dict) -> dict:
        """
        Applies guided perturbation to parameters sensitive to the Fixed Point.
        """
        mutated_scenario = copy.deepcopy(scenario_prototype)
        logger.debug(f"Applying Intelligent Fuzzing targeting FP: {target_fp.get('sub_type')}")
        
        # Example: If targeting Safe Headway, aggressively fuzz NPC braking and Ego speed
        for participant in mutated_scenario.get("participants", []):
            if participant["role"] == "NPCVehicle":
                # Push the NPC speed closer to its lower bound (harder braking)
                speed_range = participant.get("speed_range", {})
                current_val = speed_range.get("current_val", speed_range["max_val"])
                # Gradient-like push towards boundary
                new_val = current_val - (self.step_size * (speed_range["max_val"] - speed_range["min_val"]))
                participant["speed_range"]["current_val"] = max(new_val, speed_range["min_val"])
                
        return mutated_scenario


class StructuralMutator:
    """
    Handles Global Exploration.
    Triggered when NSGA-II detects low crowding distance (diversity stall).
    """
    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    def mutate(self, scenario_prototype: dict) -> dict:
        """
        Injects high-level semantic shifts (e.g., Weather, Actor Type).
        """
        mutated_scenario = copy.deepcopy(scenario_prototype)
        logger.debug("Applying Structural Mutation for Global Exploration.")
        
        # 1. Environmental Shift
        weathers = ["Clear", "Rain", "Fog", "Snow"]
        current_weather = mutated_scenario["environment_context"].get("weather", "Clear")
        weathers.remove(current_weather) if current_weather in weathers else None
        mutated_scenario["environment_context"]["weather"] = random.choice(weathers)
        
        # 2. Participant Role/Type Shift
        for participant in mutated_scenario.get("participants", []):
            if participant["role"] == "NPCVehicle" and random.random() < 0.5:
                # Change vehicle type to alter kinematic footprint
                types = ["Car", "Truck", "Motorcycle"]
                mutated_scenario["environment_context"]["friction_coefficient"] = 0.6 # e.g. slippery
                participant["vehicle_type"] = random.choice(types)
                
        return mutated_scenario
