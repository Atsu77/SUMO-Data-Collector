import math
import os
import xml.etree.ElementTree as ET

class SumoNetGenerator:
    LANE_WIDTH = 3.2

    def __init__(self, number_of_lanes, road_length):
        self.number_of_lanes = number_of_lanes
        self.road_length = road_length
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.output_path = os.path.join(self.current_path, "../../simuration_config")
        self.net_file = "net.net.xml"

    def generate_net_file(self):
        root = ET.Element("net")
        self.set_net_attributes(root)
        self.add_junctions(root)
        self.add_edges(root)
        self.write_net_file(root)

    def set_net_attributes(self, root):
        root.set("version", "1.0")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("xsi:noNamespaceSchemaLocation", "http://sumo.dlr.de/xsd/net_file.xsd")

    def add_junctions(self, root):
        ET.SubElement(root, "junction", id="J0", type="dead_end", x="0.0", y="0.0", shape=f"0.0,0.0 0.0,{self.calculate_junction_y()}")
        ET.SubElement(root, "junction", id="J1", type="dead_end", x=f"{self.road_length}", y="0.0", shape=f"{self.road_length},{self.calculate_junction_y()} {self.road_length},0.0")

    def add_edges(self, root):
        edge = ET.SubElement(root, "edge")
        edge.set("id", "E0")
        edge.set("from", "J0")
        edge.set("to", "J1")
        edge.set("priority", "1")
        lane = ET.SubElement(edge, "lane", id="E0_0", index="0", length=str(self.road_length), speed="13.89", shape=f"0.0,{self.calculate_lane_y(0)} {self.road_length},{self.calculate_lane_y(0)}")

        for i in range(1, self.number_of_lanes):
            lane = ET.SubElement(edge, "lane", id=f"E0_{i}", index=str(i))
            lane.set("length", str(self.road_length))
            lane.set("speed", "13.89")
            lane.set("shape", f"0.0,{self.calculate_lane_y(i)} {self.road_length},{self.calculate_lane_y(i)}")

    def write_net_file(self, root):
        tree = ET.ElementTree(root)
        output_path = os.path.join(self.output_path, self.net_file)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)

    def calculate_lane_y(self, lane_index):
        return round((self.LANE_WIDTH * (self.number_of_lanes - lane_index) - self.LANE_WIDTH / 2) * 100) / 100

    def calculate_junction_y(self):
        return round(self.LANE_WIDTH * self.number_of_lanes * 100) / 100
