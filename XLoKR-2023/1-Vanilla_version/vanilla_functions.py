import subprocess
import re
import pandas as pd
import pygraphviz as pgv
import pandas as pd
import os
from IPython.display import Image

def visualize_file(input_file, pred_name, output_filename, argu=False):
    edges = []
    try:
        with open(input_file, 'r') as file:
            for line in file:
                # Extract edges that match the pattern "predicate_name(source, target)"
                match = re.match(r'{}\(([^,]+),([^)]+)\)'.format(pred_name), line)
                if match:
                    source = match.group(1)
                    target = match.group(2)
                    
                    # Switching the source and target if the argu parameter is True
                    if argu:
                        source, target = target, source

                    edges.append((source, target))
    except:
        pattern = r'{}\s*\(([^,]+),\s*([^)]+)\)'.format(pred_name)
        edges = re.findall(pattern, input_file)
        # Switching the source and target if the argu parameter is True
        if argu:
            edges = [(target, source) for source, target in edges]

    edge_df = pd.DataFrame(edges, columns=['source', 'target'])
    G = pgv.AGraph(directed=True)
    for _, row in edge_df.iterrows():
        # Adding edges from the dataframe
        edge_dir = "back" if argu else "forward"
        G.add_edge(row['source'], row['target'], dir=edge_dir)
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
        if node_type == "drawn" or node_type == "undefined" or node_type == "pk":
            nodes_list = re.findall(fr'{node_type}\((\w+)\)', undefined_part)
            nodes_status[node_type] = nodes_list
        else:
            nodes_list = re.findall(fr'{node_type}\((\w+)\)', true_part)
            nodes_status[node_type] = nodes_list

    return nodes_status


def color_graph(file_path, output_name,nodes_status, node_color, edge_color):
    G = pgv.AGraph(file_path)
    
    color_node_map_game = {
        'red': '#FFAAAA', 'green': '#AAFFAA', 'yellow': '#FFFFAA', 
        "orange": "#bfefff", "blue": "#ffdaaf", "black": "#000000", 
        "white": "#ffffff", "gray": '#b7b7b7'
    }

    color_edge_map_game = {
        'red': '#CC0000', 'green': '#00BB00', 'yellow': '#AAAA00', 
        "gray": '#b7b7b7', "orange": "#cc8400", "blue": "#006ad1",
        "dark_gray": "#A9A9A9","black": "#000000", "dark_yellow":"#000080"
    }
    
    if nodes_status and node_color:
        for status, nodes in nodes_status.items():
            for node in nodes:
                G.get_node(node).attr['fillcolor'] = color_node_map_game[node_color[status]]
                G.get_node(node).attr['style'] = 'filled'
                if color_node_map_game[node_color[status]] == '#000000':  
                    G.get_node(node).attr['fontcolor'] = '#ffffff'


    if edge_color:
        for edge in G.edges():
            source_node = G.get_node(edge[0])
            target_node = G.get_node(edge[1])
            source_color = None
            target_color = None

            for color, hex_color in color_node_map_game.items():
                if source_node.attr['fillcolor'] == hex_color:
                    source_color = color
                if target_node.attr['fillcolor'] == hex_color:
                    target_color = color

            edge_color_default = 'gray'
            if source_color and target_color:
                selected_edge_color = edge_color.get((source_color, target_color), edge_color_default)
                current_edge = G.get_edge(edge[0], edge[1])
                current_edge.attr['color'] = color_edge_map_game[selected_edge_color]
                if selected_edge_color == 'gray':
                    current_edge.attr['style'] = 'dashed'

    base_file_name = file_path.split(".")[0]
    output_file_path_dot = "output/"+ output_name + "_graph_colored" + ".dot"
    output_file_path_png = "output/"+ output_name + "_graph_colored" + ".png"
    
    G.write(output_file_path_dot)
    G.draw(output_file_path_png, prog='dot', format='png')
    
    
def change_edge_direction(dot_file_path, output_file_path):
    # Load the .dot file
    graph = pgv.AGraph(dot_file_path)
    
    # Iterate over edges and modify the direction
    for edge in graph.edges():
        if edge.attr['dir'] == 'forward':
            edge.attr['dir'] = 'back'
        elif edge.attr['dir'] == 'back':
            edge.attr['dir'] = 'forward'

    base_file_name = dot_file_path.split(".")[0]
    output_file_path_dot = base_file_name+ "_reverse"+".dot"
    output_file_path_png = base_file_name+ "_reverse"+".png"
    
    graph.write(output_file_path_dot)
    graph.draw(output_file_path_png, prog='dot', format='png')