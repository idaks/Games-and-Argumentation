import subprocess
import re
import pandas as pd
import pygraphviz as pgv
import pandas as pd
import os
from IPython.display import Image

def visualize_file(input_file,pred_name,output_filename):
    edges = []
    try:
        with open(input_file, 'r') as file:
            for line in file:
                # Extract edges that match the pattern "predicate_name(source, target)"
                match = re.match(r'{}\(([^,]+),([^)]+)\)'.format(pred_name), line)
                if match:
                    source = match.group(1)
                    target = match.group(2)
                    edges.append((source, target))
    except:
        pattern = r'{}\s*\(([^,]+),\s*([^)]+)\)'.format(pred_name)
        edges = re.findall(pattern, input_file)
    edge_df = pd.DataFrame(edges, columns=['source', 'target'])
    G = pgv.AGraph(directed=True)
    for _, row in edge_df.iterrows():
        # Adding edges from the dataframe
        G.add_edge(row['source'], row['target'], dir="forward")
        G.write('output/{}.dot'.format(output_filename))
        G.draw('output/{}.png'.format(output_filename), prog='dot', format='png')

def run_command(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    output = result.stdout.decode()
    return output


def get_nodes_status(string, node_types):
    nodes_status = {}
    
    # Extract the true part and undefined part from the string
    true_part_match = re.search(r'True: {(.*?)}', string)
    true_part = true_part_match.group(1) if true_part_match else ""

    undefined_part_match = re.search(r'Undefined: {(.*?)}', string)
    undefined_part = undefined_part_match.group(1) if undefined_part_match else ""
    
    # Go through each node type and find its occurrences in the appropriate part
    for node_type in node_types:
        if node_type == "drawn":
            nodes_list = re.findall(fr'{node_type}\((\w+)\)', undefined_part)
            nodes_status[node_type] = nodes_list
        else:
            nodes_list = re.findall(fr'{node_type}\((\w+)\)', true_part)
            nodes_status[node_type] = nodes_list

    return nodes_status

def color_nodes(file_path, nodes_status, node_color_schema):
    G = pgv.AGraph(file_path)
    color_node_map_game = {'red': '#FFAAAA', 'green': '#AAFFAA', 'yellow': '#FFFFAA', "orange":"#bfefff", "blue":"#ffdaaf"}
    for status, nodes in nodes_status.items():
        for node in nodes:
            G.get_node(node).attr['fillcolor'] = color_node_map_game[node_color_schema[status]]
            G.get_node(node).attr['style'] = 'filled'
    base_file_name = file_path.split(".")[0]
    output_file_path_dot = base_file_name + "_node_colored" + ".dot"
    output_file_path_png = base_file_name + "_node_colored" + ".png"
    G.write(output_file_path_dot)
    G.draw(output_file_path_png, prog='dot', format='png')
    
    
def color_edges(file_path, edge_color_schema):
    G = pgv.AGraph(file_path)
    color_node_map_game = {'red': '#FFAAAA', 'green': '#AAFFAA', 'yellow': '#FFFFAA', "orange":"#bfefff", "blue":"#ffdaaf"}
    color_edge_map_game = {'red': '#CC0000', 'green': '#00BB00', 'yellow': '#AAAA00', "gray": '#b7b7b7', "orange":"#cc8400", "blue":"#006ad1"}

    for edge in G.edges():
        source_node = G.get_node(edge[0])
        target_node = G.get_node(edge[1])
        source_color = None
        target_color = None
        
        # Determine the source and target colors
        for color, hex_color in color_node_map_game.items():
            if source_node.attr['fillcolor'] == hex_color:
                source_color = color
            if target_node.attr['fillcolor'] == hex_color:
                target_color = color
        
        # Set default edge color to avoid black edges
        edge_color_default = 'gray'
        if source_color and target_color:
            edge_color = edge_color_schema.get((source_color, target_color), edge_color_default)
            G.get_edge(edge[0], edge[1]).attr['color'] = color_edge_map_game[edge_color]
            current_edge = G.get_edge(edge[0], edge[1])
            current_edge.attr['color'] = color_edge_map_game[edge_color]
            if edge_color == 'gray':
                current_edge.attr['style'] = 'dashed'

    base_file_name = file_path.split(".")[0]
    output_file_path_dot = base_file_name + "_edge_colored" + ".dot"
    output_file_path_png = base_file_name + "_edge_colored" + ".png"
    
    G.write(output_file_path_dot)
    G.draw(output_file_path_png, prog='dot', format='png')

