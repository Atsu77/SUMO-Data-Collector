import math
import os
import xml.etree.ElementTree as ET

class SumoNetGenerator:
    LANE_WIDTH = 3.2

    def __init__(self, number_of_lanes, road_length):
        self.number_of_lanes = number_of_lanes
        self.road_length = road_length
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.output_path = os.path.join(self.current_path, "../../simulation")
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
        juction_0 = ET.SubElement(root, "junction")
        juction_0.set("id", "J0")
        juction_0.set("type", "dead_end")
        juction_0.set("x", "0.0")
        juction_0.set("y", "0.0")
        juction_0.set("shape", f"0.0,0.0 0.0,{self.calculate_junction_y()}")
        juction_1 = ET.SubElement(root, "junction")
        juction_1.set("id", "J1")
        juction_1.set("type", "dead_end")
        juction_1.set("x", f"{self.road_length}")
        juction_1.set("y", "0.0")
        juction_1.set("shape", f"0.0,0.0 0.0,{self.calculate_junction_y()}")


    def add_edges(self, root):
        edge = ET.SubElement(root, "edge")
        edge.set("id", "E0")
        edge.set("from", "J0")
        edge.set("to", "J1")
        edge.set("priority", "1")

        lane = ET.SubElement(edge, "lane")
        lane.set("id", "E0_0")
        lane.set("index", "0")
        lane.set("length", str(self.road_length))
        lane.set("speed", "13.89")
        lane.set("shape", f"0.0,{self.calculate_lane_y(0)} {self.road_length},{self.calculate_lane_y(0)}")

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


class SumoRowGenerator:
    def __init__(self, maxSpeed, vehcle_per_hour, begin, end, edge):
        self.maxSpeed = maxSpeed
        self.vehcle_per_hour = vehcle_per_hour
        self.begin = begin
        self.end = end
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.output_path = os.path.join(self.current_path, "../../simulation")
        self.rou_file = "rou.rou.xml"
        self.edge = edge

    def generate_rou_file(self):
        root = ET.Element("routes")
        self.set_v_type(root)
        self.add_flow(root)
        self.write_rou_file(root)

    def set_v_type(self, root):
        v_type = ET.SubElement(root, "vType")
        v_type.set("id", "Car")
        v_type.set("length", "5.0")
        v_type.set("maxSpeed", str(self.maxSpeed))
        v_type.set("vClass", "passenger")

    def add_flow(self, root):
        flow = ET.SubElement(root, "flow")
        flow.set("id", "flow")
        flow.set("type", "Car")
        flow.set("begin", str(self.begin))
        flow.set("end", str(self.end))
        flow.set("vehsPerHour", str(self.vehcle_per_hour))
        ET.SubElement(flow, "route", edges=self.edge)

    def write_rou_file(self, root):
        tree = ET.ElementTree(root)
        output_path = os.path.join(self.output_path, self.rou_file)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)

class SumocfgGenerator:
    def __init__(self, net_file, rou_file, begin, end, step_length):
        self.net_file = net_file
        self.rou_file = rou_file
        self.begin = begin
        self.end = end
        self.step_length = step_length
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.output_path = os.path.join(self.current_path, "../../simulation")
        self.data_output_path = os.path.join(self.current_path, "data")
        self.conf_file = "sumocfg"

    def generate_conf_file(self):
        root = ET.Element("configuration")
        self.set_input(root)
        self.set_time(root)
        self.set_output(root)
        self.write_conf_file(root)

    def set_input(self, root):
        input = ET.SubElement(root, "input")
        ET.SubElement(input, "net-file", value=self.net_file)
        ET.SubElement(input, "route-files", value=self.rou_file)

    def set_time(self, root):
        time = ET.SubElement(root, "time")
        time.set("begin", self.begin)
        time.set("end", self.end)
        time.set("step-length", self.step_length)

    def set_output(self, root):
        output = ET.SubElement(root, "output")
        fcd_output = ET.SubElement(output, "fcd-output")
        data_output_path = os.path.join(self.data_output_path, "fcd.xml")
        fcd_output.set("value", f"{str(data_output_path)}")
        fcd_output_acceleration = ET.SubElement(output, "fcd-output.acceleration")
        fcd_output_acceleration.set("value", "true")

    def write_conf_file(self, root):
        tree = ET.ElementTree(root)
        output_path = os.path.join(self.output_path, self.conf_file)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)

