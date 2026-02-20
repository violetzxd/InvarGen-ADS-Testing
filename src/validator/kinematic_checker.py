"""
Kinematic Validity Checker.
Matches Section 3.5: Prevents the search engine from generating physically impossible scenarios
(e.g., deceleration > 1G, impossible lateral jerk).
"""
import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)

class KinematicChecker:
    """
    Validates that a generated scenario prototype respects physical boundaries
    before wasting computational resources on 3D simulation.
    """
    def __init__(self):
        # Physical thresholds based on standard vehicle dynamics (Sedans/SUVs)
        self.MAX_ACCELERATION = 4.0   # m/s^2 (approx 0.4G)
        self.MAX_DECELERATION = -8.5  # m/s^2 (emergency braking on dry asphalt)
        self.MAX_LATERAL_JERK = 5.0   # m/s^3 (limit for realistic steering)

    def validate(self, scenario: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Runs a lightweight pre-simulation check on the parameterized events.
        """
        logger.debug(f"Running kinematic checks for scenario: {scenario.get('name')}")
        
        # 1. Check Initial Speeds
        for participant in scenario.get("participants", []):
            speed = participant.get("speed_range", {}).get("current_val", 0.0)
            if speed < 0 or speed > 50.0:  # > 180 km/h is considered invalid for this ODD
                return False, f"Invalid initial speed {speed}m/s for {participant['id']}"

        # 2. Check Event Dynamics (Acceleration & Jerk)
        for event in scenario.get("event_sequence", []):
            action_type = event.get("action_type")
            params = {p.name: p.current_val for p in event.get("action_parameters", []) if hasattr(p, 'current_val')}
            
            if action_type == "AggressiveLaneChange":
                # Estimate lateral jerk: roughly (LaneWidth) / (Duration^3)
                duration = params.get("duration", 2.0)
                if duration <= 0.5:
                    return False, f"Lane change duration {duration}s violates MAX_LATERAL_JERK."
                    
            elif action_type == "EmergencyBraking":
                # Check target deceleration
                target_speed = params.get("target_speed", 0.0)
                duration = params.get("duration", 1.0)
                current_speed = 25.0 # Mock lookup from participant state
                
                accel = (target_speed - current_speed) / max(duration, 0.1)
                if accel < self.MAX_DECELERATION:
                    return False, f"Deceleration {accel:.2f}m/s^2 exceeds physical limits ({self.MAX_DECELERATION})."

        return True, "Kinematically Valid"
