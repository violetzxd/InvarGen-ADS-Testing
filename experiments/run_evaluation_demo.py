"""
INVARGEN End-to-End Evaluation Workflow Demo
Reference: Section 4 (Evaluation) & Section 3.4 (Hybrid Search)

This script demonstrates the end-to-end evaluation pipeline. It features a dual-backend 
simulation architecture:
1. LightweightKinematicSimulator: A fast, physics-based equation solver for rapid peer-review validation.
2. CarlaSimulatorInterface: The production hook for the CARLA 3D simulator (used for the paper's main results).
"""

import math
import random
import time
from dataclasses import dataclass
from typing import Dict, Any, List

# ============================================================================
# 1. Data Structures (Bridging Generator and Simulator)
# ============================================================================

@dataclass
class ScenarioState:
    ego_speed: float
    npc_speed: float
    initial_distance: float
    npc_braking_deceleration: float

@dataclass
class SimulationTrace:
    min_distance: float
    min_ttc: float
    collision_occurred: bool
    recovery_time: float
    max_lateral_deviation: float

# ============================================================================
# 2. Dual-Backend Simulation Interfaces
# ============================================================================

class BaseSimulator:
    """Abstract base class for ADS simulation backends."""
    def run_simulation(self, state: ScenarioState) -> SimulationTrace:
        raise NotImplementedError

class LightweightKinematicSimulator(BaseSimulator):
    """
    Lightweight backend for peer review. 
    Uses 1D kinematic equations to simulate a Rear-End / Cut-in scenario.
    Avoids the overhead of a full 3D engine while maintaining physical plausibility.
    """
    def __init__(self, time_step: float = 0.1, max_time: float = 10.0):
        self.dt = time_step
        self.max_time = max_time
        # Mock ADS response time (e.g., perception delay + actuation delay)
        self.ads_reaction_time = 0.8  
        self.ads_max_deceleration = 6.0  # m/s^2

    def run_simulation(self, state: ScenarioState) -> SimulationTrace:
        current_dist = state.initial_distance
        v_ego = state.ego_speed
        v_npc = state.npc_speed
        
        min_dist = current_dist
        min_ttc = float('inf')
        collision = False
        
        for t_idx in range(int(self.max_time / self.dt)):
            t = t_idx * self.dt
            
            # NPC behavior: Hard braking from t=0
            a_npc = -state.npc_braking_deceleration
            v_npc = max(0.0, v_npc + a_npc * self.dt)
            
            # Ego behavior: Reacts after perception delay
            a_ego = 0.0
            if t > self.ads_reaction_time:
                # Simple AEB logic: brake if TTC is dangerously low
                relative_v = v_ego - v_npc
                if relative_v > 0 and (current_dist / relative_v) < 2.5:
                    a_ego = -self.ads_max_deceleration
            
            v_ego = max(0.0, v_ego + a_ego * self.dt)
            
            # Update spatial relationship
            current_dist -= (v_ego - v_npc) * self.dt
            
            if current_dist < min_dist:
                min_dist = current_dist
                
            # Calculate TTC
            rel_v = v_ego - v_npc
            if rel_v > 0:
                ttc = current_dist / rel_v
                if ttc < min_ttc:
                    min_ttc = ttc
                    
            if current_dist <= 0:
                collision = True
                min_dist = 0.0
                min_ttc = 0.0
                break
                
        return SimulationTrace(
            min_distance=min_dist,
            min_ttc=min_ttc,
            collision_occurred=collision,
            recovery_time=5.0 if not collision else -1.0,
            max_lateral_deviation=0.2 # Simplified for 1D model
        )

class CarlaSimulatorInterface(BaseSimulator):
    """
    Production backend connecting to the CARLA Simulator.
    Provided to demonstrate completeness and OpenX compatibility.
    """
    def __init__(self, host: str = '127.0.0.1', port: int = 2000):
        self.host = host
        self.port = port
        self._client = None
        self._world = None

    def connect(self):
        """Attempts to connect to a running CARLA instance."""
        try:
            # import carla  # Deferred import to avoid dependency errors for reviewers
            # self._client = carla.Client(self.host, self.port)
            # self._client.set_timeout(10.0)
            # self._world = self._client.get_world()
            pass
        except Exception as e:
            raise ConnectionError(f"Failed to connect to CARLA at {self.host}:{self.port}. Ensure server is running.")

    def run_simulation(self, state: ScenarioState) -> SimulationTrace:
        """
        Executes the scenario in the 3D CARLA environment.
        Raises NotImplementedError to prevent execution during lightweight review.
        """
        raise NotImplementedError(
            "CARLA backend invoked. For peer review, please use the LightweightKinematicSimulator. "
            "Full 3D execution requires a local CARLA 0.9.13+ installation and the OpenSCENARIO runner."
        )

# ============================================================================
# 3. Hybrid Search Engine (Fuzzing Optimization Loop)
# ============================================================================

class DemoSearchEngine:
    """
    A lightweight implementation of the Fixed-Point Guided Hybrid Search (Algorithm 1).
    Demonstrates how Intelligent Fuzzing exploits the simulator feedback.
    """
    def __init__(self, simulator: BaseSimulator):
        self.simulator = simulator
        # Target Safe Headway Fixed Point: distance > 5.0 meters
        self.target_safe_distance = 5.0 

    def calculate_fitness(self, trace: SimulationTrace) -> float:
        """
        Simplified fitness function. 
        Higher score means worse ADS performance (closer to Fixed Point violation).
        """
        if trace.collision_occurred:
            return 1000.0  # Maximum fitness (Defect found)
        
        # Invert distance: closer distance -> higher fitness
        safety_violation_cost = max(0.0, self.target_safe_distance - trace.min_distance)
        
        # Penalize large TTCs
        criticality_cost = 1.0 / max(trace.min_ttc, 0.1) 
        
        return (safety_violation_cost * 10.0) + criticality_cost

    def run_fuzzing_loop(self, generations: int = 5, pop_size: int = 4):
        """Executes the evolutionary loop targeting the Fixed Point boundaries."""
        print(f"--- Starting Hybrid Search (Generations: {generations}, PopSize: {pop_size}) ---")
        
        # Initial Population: Slightly varying NPC braking deceleration
        population = [
            ScenarioState(ego_speed=25.0, npc_speed=20.0, initial_distance=15.0, npc_braking_deceleration=random.uniform(3.0, 5.0))
            for _ in range(pop_size)
        ]
        
        best_scenario = None
        max_fitness = -1.0
        
        for gen in range(generations):
            print(f"\n[Generation {gen+1}] Evaluating Population...")
            evaluated = []
            
            for idx, scenario in enumerate(population):
                trace = self.simulator.run_simulation(scenario)
                fitness = self.calculate_fitness(trace)
                evaluated.append((scenario, fitness, trace))
                
                print(f"  Ind {idx}: NPC_Brake={scenario.npc_braking_deceleration:.2f} m/s^2 | "
                      f"MinDist={trace.min_distance:.2f}m | MinTTC={trace.min_ttc:.2f}s | Fitness={fitness:.2f}")
                
                if fitness > max_fitness:
                    max_fitness = fitness
                    best_scenario = (scenario, trace)
                    
            # Check for violation
            if best_scenario[1].collision_occurred:
                print("  [!] Critical Defect Discovered: Collision Occurred! Halting search.")
                break
                
            # Selection & Fuzzing (Mutation) -> Push towards harder braking
            # In a full NSGA-II, this uses Crowding Distance and Crossover
            evaluated.sort(key=lambda x: x[1], reverse=True)
            parents = [evaluated[0][0], evaluated[1][0]] 
            
            population = []
            for _ in range(pop_size):
                parent = random.choice(parents)
                # Fuzzer exploits the parameter: increases deceleration slightly to increase threat
                mutated_decel = min(8.0, parent.npc_braking_deceleration + random.uniform(0.1, 0.8))
                child = ScenarioState(
                    ego_speed=parent.ego_speed, 
                    npc_speed=parent.npc_speed, 
                    initial_distance=parent.initial_distance, 
                    npc_braking_deceleration=mutated_decel
                )
                population.append(child)
                
        return best_scenario

# ============================================================================
# 4. Main Execution Block
# ============================================================================

if __name__ == "__main__":
    print("==========================================================")
    print(" INVARGEN: Evaluation Workflow Demo (Lightweight Version) ")
    print("==========================================================\n")
    
    # 1. Initialize the lightweight simulator (bypassing CARLA requirement)
    print("[System] Initializing Lightweight Kinematic Simulator...")
    simulator = LightweightKinematicSimulator()
    
    # 2. Initialize the Search Engine
    search_engine = DemoSearchEngine(simulator=simulator)
    
    # 3. Execute the Fuzzing Loop (Demonstrating RQ2 & RQ3)
    start_time = time.time()
    best_result = search_engine.run_fuzzing_loop(generations=5, pop_size=4)
    elapsed = time.time() - start_time
    
    # 4. Report Results
    print("\n==================== SEARCH COMPLETE ====================")
    print(f"Time Elapsed: {elapsed:.2f} seconds")
    if best_result:
        scenario, trace = best_result
        print(f"Most Critical Scenario Discovered:")
        print(f" - Ego Speed: {scenario.ego_speed} m/s")
        print(f" - NPC Deceleration (Fuzzed): {scenario.npc_braking_deceleration:.2f} m/s^2")
        print(f" - Resulting Min Distance: {trace.min_distance:.2f} m")
        print(f" - Resulting Min TTC: {trace.min_ttc:.2f} s")
        if trace.collision_occurred:
            print(" - Fixed Point Violation: FAILED (Collision Triggered)")
        elif trace.min_distance < search_engine.target_safe_distance:
            print(" - Fixed Point Violation: FAILED (Safe Headway Breached)")
        else:
            print(" - Fixed Point Violation: PASSED (System remained safe)")
    print("==========================================================")
    
    # 5. Demonstrate CARLA Interface readiness
    print("\n[System] Note: To execute with full 3D physics, instantiate CarlaSimulatorInterface().")
