import subprocess
import re
import pandas as pd
import pygraphviz as pgv
import pandas as pd
import os
import datetime
import shutil

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


def color_graph(file_path, output_name,nodes_status, node_color, edge_color, layout="dot"):
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
    
    for node in G.nodes():
        node.attr['fillcolor'] = "#ffffff"
        node.attr['style'] = 'filled'
    
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
    G.draw(output_file_path_png, prog=layout, format='png')
    
    
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
    
    
def count_sets(s: str) -> int:
    sets_found = re.findall(r'\{[^}]*\}', s)
    return len(sets_found)

def count_cycles(s: str) -> int:
    cycle_found = re.findall(r'cycle\([^)]*\)', s)
    return len(cycle_found)

def extract_sets(input_string):
    # Extract all the characters inside the curly braces
    sets = re.findall(r'\{[^}]*\}', input_string)

    # Dictionary to store the results
    result_dict = {}

    for idx, s in enumerate(sets, 1):
        elements = [re.search(r'\((.)\)', el).group(1) for el in s.split(',')]
        key = f'pw{idx}'
        result_dict[key] = elements
    return result_dict


import os
import ipywidgets as widgets
from IPython.display import display, Image

def display_colored_graphs(filename,pw_dict, layout="dot"):
    
    # Create the subfolder
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    subfolder = os.path.join("output", timestamp)
    os.makedirs(subfolder, exist_ok=True)
    
    
    kernel_node_color = {
        'k': 'black'
    }
    kernel_edge_color = {
        ('white', 'white'): 'gray',
        ('white', 'black'): 'dark_gray',
        ('black', 'white'): 'black'
    }
    
    visualize_file(filename, "edge", "plain_graph")
    
    for idx, (key, nodes) in enumerate(pw_dict.items(), 1):
        kernel_name = f"kernel_{key}"
        kernel_nodes_status = {"k": nodes}
        color_graph(os.path.join("output", "plain_graph.dot"), timestamp+"/"+kernel_name, kernel_nodes_status, kernel_node_color, kernel_edge_color, layout)
    
    # Update the file search pattern to the new subfolder
    files = sorted([f for f in os.listdir(subfolder) if f.startswith("kernel_pw") and f.endswith("_graph_colored.png")])

    # Adjust display_image function to account for the new subfolder
    def display_image(index):
        file_path = os.path.join(subfolder, files[index-1])
        img = Image(filename=file_path)
        title = "pw" + str(index)
        print(title)
        display(img)

    # Create a slider to navigate through the images
    widgets.interact(display_image, index=widgets.IntSlider(min=1, max=len(files), step=1, value=1, description='Slider'))

def delete_timestamped_subfolders(directory="output"):
    # Regular expression pattern to match the timestamp pattern (YYYYMMDD_HHMMSS)
    pattern = r"\d{8}_\d{6}"
    
    for dir_name in os.listdir(directory):
        dir_path = os.path.join(directory, dir_name)
        if os.path.isdir(dir_path) and re.match(pattern, dir_name):
            shutil.rmtree(dir_path)
            print(f"Deleted {dir_path}")
