"""
Multi-Objective Fitness Calculation for INVARGEN.
Implements Equations (1) to (4) from Section 3.4.1 of the paper.
"""
import math
import numpy as np
from typing import Dict, Any

class FitnessEvaluator:
    def __init__(self, lambda_penalty: float = 1.2):
        self.lambda_penalty = lambda_penalty

    def evaluate(self, sim_trace: Dict[str, Any], target_fps: list) -> tuple:
        """
        Evaluates a simulation trace and returns the 4D objective vector.
        Note: NSGA-II standardizes on MINIMIZATION. We negate maximization targets.
        """
        j_safety = self._calc_j_safety(sim_trace, target_fps)
        j_recovery = self._calc_j_recovery(sim_trace, target_fps)
        j_crit = self._calc_j_crit(sim_trace)
        j_div = self._calc_j_div(sim_trace) # Usually calculated at population level, placeholder here
        
        # Return tuple of objectives (J_safety, J_recovery, J_crit, J_div)
        return (j_safety, j_recovery, j_crit, j_div)

    def _calc_j_safety(self, sim_trace: Dict[str, Any], target_fps: list) -> float:
        """
        Eq. (1): Safety Violation Cost.
        Calculates the time-integral of the violation magnitude.
        """
        violation_integral = 0.0
        # Mock calculation: Iterate over time steps in trace
        for step in sim_trace.get("steps", []):
            dist = step.get("distance_to_front", 100.0)
            d_safe = 10.0 # Extracted from the Fixed Point definition
            
            # v(t) = max(0, d_safe - dist(t))
            v_t = max(0.0, d_safe - dist)
            if v_t > 0:
                # v(t) * e^(lambda * v(t))
                violation_integral += v_t * math.exp(self.lambda_penalty * v_t)
                
        # We negate the value to minimize it (i.e., finding scenarios with maximum violation)
        return -violation_integral

    def _calc_j_recovery(self, sim_trace: Dict[str, Any], target_fps: list) -> float:
        """
        Eq. (2): Recovery Failure Cost.
        """
        t_event = sim_trace.get("perturbation_time", 0.0)
        t_stable = sim_trace.get("restabilization_time", -1.0)
        t_max = sim_trace.get("max_sim_time", 20.0)
        
        if t_stable > 0:
            # If recovered, cost is the time taken to recover
            # We negate it because longer recovery time = worse ADS performance = better test case
            return -(t_stable - t_event)
        else:
            # If failure (timeout), apply massive penalty based on final deviation
            dev_final = sim_trace.get("final_deviation", 5.0)
            return -(t_max + (5.0 * dev_final)) # Beta = 5.0

    def _calc_j_crit(self, sim_trace: Dict[str, Any]) -> float:
        """
        Eq. (3): Criticality Index based on Minimum TTC.
        """
        min_ttc = sim_trace.get("min_ttc", 10.0)
        # Prevent division by zero, min TTC is capped at 0.1
        min_ttc = max(min_ttc, 0.1)
        # Minimize the inverse of TTC (i.e., maximize criticality)
        return - (1.0 / min_ttc)

    def _calc_j_div(self, sim_trace: Dict[str, Any]) -> float:
        """
        Eq. (4): Semantic Diversity Score.
        In a real run, this requires access to the entire population archive.
        Returning 0.0 here; handled in the NSGA-II population ranking phase.
        """
        return 0.0
