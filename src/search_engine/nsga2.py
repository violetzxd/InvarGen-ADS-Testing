"""
The core Multi-Objective Search Optimization Loop (NSGA-II).
Matches Algorithm 1 and Section 3.4.2 of the paper.
"""
import logging
from typing import List, Dict, Any
from .fitness import FitnessEvaluator
from .operators import IntelligentFuzzer, StructuralMutator

logger = logging.getLogger(__name__)

class FixedPointGuidedNSGA2:
    def __init__(self, pop_size: int = 50, max_gen: int = 30):
        self.pop_size = pop_size
        self.max_gen = max_gen
        self.evaluator = FitnessEvaluator()
        self.fuzzer = IntelligentFuzzer()
        self.mutator = StructuralMutator()
        
    def optimize(self, initial_prototypes: List[Dict[str, Any]], target_fps: list) -> List[Dict[str, Any]]:
        """
        The main evolutionary loop (Algorithm 1).
        """
        population = initial_prototypes[:self.pop_size]
        logger.info(f"Starting NSGA-II Optimization with PopSize={self.pop_size}, MaxGen={self.max_gen}")
        
        for generation in range(self.max_gen):
            logger.info(f"--- Generation {generation+1}/{self.max_gen} ---")
            
            # 1. Evaluation Phase
            evaluated_population = []
            for scenario in population:
                # In real execution, this calls the Carla/Panosim simulator
                sim_trace = self._mock_simulate(scenario) 
                
                # Calculate J(S) = (J_safety, J_recovery, J_crit, J_div)
                fitness_vector = self.evaluator.evaluate(sim_trace, target_fps)
                evaluated_population.append({
                    "scenario": scenario,
                    "fitness": fitness_vector,
                    "crowding_distance": 0.0 # Placeholder
                })
                
            # 2. Fast Non-Dominated Sort & Crowding Distance (NSGA-II core)
            fronts = self._fast_non_dominated_sort(evaluated_population)
            self._assign_crowding_distance(fronts)
            
            # Select parents for next generation (Tournament Selection)
            parents = self._tournament_selection(fronts, num_parents=self.pop_size)
            
            # 3. Offspring Generation (The Hybrid Mechanism)
            offspring = []
            while len(offspring) < self.pop_size:
                parent = random.choice(parents)
                
                # Operator Selection based on Diversity (Crowding Distance)
                # If a solution is too crowded (stuck in local optima), explore globally!
                if parent["crowding_distance"] < 0.5: # Threshold for diversity stall
                    # Global Exploration
                    child_scenario = self.mutator.mutate(parent["scenario"])
                else:
                    # Local Exploitation
                    # Fuzz parameters sensitive to the first target Fixed Point
                    child_scenario = self.fuzzer.fuzz(parent["scenario"], target_fps[0])
                    
                offspring.append(child_scenario)
                
            # Replace population
            population = offspring
            
        logger.info("Optimization complete. Returning Pareto-optimal scenarios.")
        # Return the first front of the last generation
        return [ind["scenario"] for ind in fronts[0]]

    # --- NSGA-II Standard Helpers (Mocked for structure demonstration) ---
    def _mock_simulate(self, scenario: dict) -> dict:
        """Mocks a simulation trace return."""
        return {"distance_to_front": random.uniform(2.0, 15.0), "min_ttc": random.uniform(0.5, 3.0), "restabilization_time": random.uniform(2.0, 10.0)}

    def _fast_non_dominated_sort(self, population: list) -> list:
        """Groups population into Pareto fronts. (Simplified mock)"""
        return [population] # Assumes all are rank 1 for this demo

    def _assign_crowding_distance(self, fronts: list):
        """Calculates diversity within a front. Assigns random values for demo."""
        for front in fronts:
            for ind in front:
                ind["crowding_distance"] = random.uniform(0.1, 1.0)

    def _tournament_selection(self, fronts: list, num_parents: int) -> list:
        """Selects best individuals based on rank and crowding distance."""
        return random.choices(fronts[0], k=num_parents)
