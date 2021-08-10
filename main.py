"""
(c) 2021 James & Anshul
Date: 8/10/2021
Name: James Rozsypal & Anshul Chauhan
Student ID: 015668339 & 016246735
Email: james.rozsypal@student.csulb.edu & anshul.chauhan@student.csulb.edu
"""

from Graph.Graph import Graph
from pathlib import Path
from SearchAlgorithms.DFSRec import DFSRec
from SearchAlgorithms.DFSNodeColor import DFSNodeColor

# Converting maze to graph

output_folder = Path("Output/")
data_folder = Path("Data/TextData/")
data = data_folder / "map.txt"

color_list = [0, 1, 2]
color_names = {0:"Red", 1:"Blue", 2:"Green"}

g = Graph(data, color_list)
g.graph_build()
size = g.graph_length()

# g.graph_summary()

# dfs = DFSRec(g, size, 2)
# dfs.DFS_recursive()

dfs_color = DFSNodeColor(g, size, color_names)
dfs_color.DFS_recursive()
