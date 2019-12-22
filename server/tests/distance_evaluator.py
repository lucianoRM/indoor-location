import re
import time
from unittest.mock import Mock

from src.core.location.geometric_location_service import GeometricLocationService
from src.core.location.oa_location_service import OALocationService
from src.core.location.reference_point import ReferencePoint
from src.core.location.simple_location_service import SimpleLocationService

optimized_ls = OALocationService(Mock())
geometric_lc = GeometricLocationService(Mock())
simple_lc = SimpleLocationService(Mock())

class Data:

    def __init__(self,  line):
        self.se = self.__get_se_id(line)
        self.tx = self.__get_tx(line)
        self.rx = self.__get_rx(line)

    def __get_se_id(self, line):
        return int(re.match(".*SE: ([0-9]*) .*", line).group(1))

    def __get_tx(self, line):
        return float(re.match(".*Tx: ([^,]*),*", line).group(1))

    def __get_rx(self, line):
        return float(re.match(".*Rx: ([^\]]*)\]*", line).group(1))

def get_time():
    return int(round(time.time() * 1000))

def split_fours(lines):
    groups = []
    inner_group = []
    i = 0
    for line in lines:
        if i > 3:
            groups.append(inner_group)
            inner_group = []
            i=0
        inner_group.append(line)
        i+=1
    if(len(inner_group) > 0):
        groups.append(inner_group)
    return groups

def compute_distance(data):
    exp = (data.tx - data.rx)/24
    return 10 ** exp

def get_position(id):
    if(id == 1):
        return (0,0)
    if(id == 2):
        return (10, 0)
    if(id == 3):
        return (0, 10)
    if(id == 4):
        return (10,10)

def build_reference_points(data_list):
    reference_points = {}
    for data in data_list:
        if data.se in reference_points:
            print("\n\nERROR\n\n")
            exit()
        reference_points[data.se] = ReferencePoint(get_position(data.se), compute_distance(data), 0)
    return reference_points.values()

file_locations = ["../../measurements/power1-00.log",
                  "../../measurements/power1-55.log",
                  "../../measurements/power2-00.log",
                  "../../measurements/power2-55.log",
                  "../../measurements/power3-00.log",
                  "../../measurements/power3-55.log"]

for file_location in file_locations:
    start = get_time()
    print("\n\nFOR " + file_location + "\n\n")
    with open(file_location, 'r') as f:
        lines = [l for l in f]
        groups = split_fours(lines)
        for group in groups:
            data_list = [Data(g) for g in group]
            reference_points = build_reference_points(data_list)
            start = get_time()
            ol = optimized_ls.locate_object(list(reference_points))
            start = get_time()
            gl = geometric_lc.locate_object(list(reference_points))
            start = get_time()
            sl = simple_lc.locate_object(list(reference_points))
            start = get_time()
            print("{0},{1},,,{2},{3},,,{4},{5}".format(ol[0], ol[1], gl[0], gl[1], sl[0], sl[1]))
