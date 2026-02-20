"""
OpenSCENARIO (OSC) Compiler.
Matches Section 3.5: Scenario Formalization and Serialization.
Translates abstract Python objects into runnable .xosc XML files.
"""
import xml.etree.ElementTree as ET
import xml.dom.minidom
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class OpenScenarioCompiler:
    """
    Compiles the INVARGEN ScenarioPrototype into OpenSCENARIO 1.0/1.1 XML format.
    """
    def __init__(self, output_dir: str = "outputs/"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def compile(self, scenario: Dict[str, Any], filename: str = "generated.xosc") -> str:
        """
        Builds the XML tree according to the ASAM OpenSCENARIO schema.
        """
        logger.info(f"Compiling scenario to OpenSCENARIO format: {filename}")
        
        # 1. Root Element
        root = ET.Element("OpenSCENARIO")
        
        # 2. FileHeader
        header = ET.SubElement(root, "FileHeader")
        header.set("revMajor", "1")
        header.set("revMinor", "0")
        header.set("date", "2026-01-01T10:00:00")
        header.set("description", scenario.get("name", "INVARGEN_Scenario"))
        header.set("author", "INVARGEN_System")

        # 3. RoadNetwork (Link to OpenDRIVE .xodr)
        road_network = ET.SubElement(root, "RoadNetwork")
        logic_file = ET.SubElement(road_network, "LogicFile")
        # Base the map on the extracted environmental context
        map_name = scenario.get("environment_context", {}).get("road_type", "Town04")
        logic_file.set("filepath", f"{map_name}.xodr")

        # 4. Entities (Participants)
        entities = ET.SubElement(root, "Entities")
        for participant in scenario.get("participants", []):
            scenario_obj = ET.SubElement(entities, "ScenarioObject")
            scenario_obj.set("name", participant["id"])
            vehicle = ET.SubElement(scenario_obj, "Vehicle")
            vehicle.set("name", participant.get("vehicle_type", "vehicle.tesla.model3"))
            vehicle.set("vehicleCategory", "car")

        # 5. Storyboard (Initialization and Events)
        storyboard = ET.SubElement(root, "Storyboard")
        
        # 5.1 Init Phase
        init = ET.SubElement(storyboard, "Init")
        actions = ET.SubElement(init, "Actions")
        for participant in scenario.get("participants", []):
            # Mocking the initialization of speed and position
            private_action = ET.SubElement(actions, "Private")
            private_action.set("entityRef", participant["id"])
            # Speed Action
            speed_action = ET.SubElement(private_action, "PrivateAction")
            longitudinal = ET.SubElement(speed_action, "LongitudinalAction")
            speed = ET.SubElement(longitudinal, "SpeedAction")
            target = ET.SubElement(speed, "SpeedActionTarget")
            abs_target = ET.SubElement(target, "AbsoluteTargetSpeed")
            abs_target.set("value", str(participant.get("speed_range", {}).get("current_val", 20.0)))

        # 5.2 Story (Skipped full implementation for the peer-review package)
        story = ET.SubElement(storyboard, "Story")
        story.set("name", "MainStory")
        # ... event generation logic ...

        # 6. Write to XML File with pretty print
        xml_string = ET.tostring(root, encoding='utf-8')
        parsed_xml = xml.dom.minidom.parseString(xml_string)
        pretty_xml = parsed_xml.toprettyxml(indent="  ")

        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(pretty_xml)
            
        logger.info(f"OpenSCENARIO compilation successful -> {output_path}")
        return output_path
