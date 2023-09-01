import re
import pandas as pd
import subprocess
import ipywidgets as widgets
from IPython.display import display, clear_output
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import pygraphviz as pgv

def read_edges_from_file(filename):
    edges = []
    with open(filename, 'r') as file:
        for line in file:
            # Extract edges that match the pattern "m(source, target)"
            match = re.match(r'm\(([^,]+),([^)]+)\)', line)
            if match:
                source = match.group(1)
                target = match.group(2)
                edges.append((source, target))
                
    edge_df = pd.DataFrame(edges, columns=['source', 'target'])
    return edge_df

def run_command(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    output = result.stdout.decode()
    return output

def to_dataframe(output):
    output = output[1:-1]

    # Split the output into separate items
    items = output.split(", ")

    # Prepare the data for DataFrame
    data = []
    for item in items:
        # Extract the elements
        elements = re.findall(r'node\((.*?),(.*?),(.*?)\)', item)[0]
        data.append(elements)

    # Create DataFrame
    df = pd.DataFrame(data, columns=['color', 'state_id', 'node_label'])
    
    df=df[['state_id', 'node_label', 'color']]
    return df

def redefine_states(state_df):
    # Count unique colors for each state_id
    color_counts = state_df.groupby('state_id')['color'].nunique()

    # Create a mapping for colors to their respective increments
    color_mapping = {'g': .1, 'r': .2}  # Adjust this mapping based on your requirement

    # Create a new state_id column
    state_df['new_state_id'] = state_df['state_id'].astype(float)

    # Apply the mapping to the color column only if there are more than one unique color for that state_id
    state_df['new_state_id'] = state_df.apply(
        lambda row: row['new_state_id'] + color_mapping.get(row['color'], 0) 
        if color_counts[row['state_id']] > 1 else row['new_state_id'], axis=1
    )

    # Replace the old state_id column with the new one
    state_df['state_id'] = state_df['new_state_id']
    state_df.drop(columns=['new_state_id'], inplace=True)
    state_df = state_df.sort_values(by='state_id')
    
    return state_df

def create_colored_graph(edge_df, state_df, mode="game", directory_path='output'):
    # Helper function to delete directory contents
    def delete_directory_contents(dir_path):
        import os
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    delete_directory_contents(file_path)
                    os.rmdir(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

    # Clear the directory contents
    delete_directory_contents(directory_path)

    # Stylesheet set up
    color_map_game = {'r': '#FFAAAA', 'g': '#AAFFAA', 'y': '#FFFFAA'}
    color_map_argumentation = {'r': '#bfefff', 'g': '#ffdaaf', 'y': '#ffffbf'}

    edge_dir_game = "forward"
    edge_dir_argumentation = "back"

    # Use different stylesheet for game and argumentation
    if mode == "game":
        color_map = color_map_game
        edge_dir = edge_dir_game
    else:
        color_map = color_map_argumentation
        edge_dir = edge_dir_argumentation

    # Create a directed graph from the first dataframe
    G = pgv.AGraph(directed=True)

    # Adding edges from the edge dataframe
    for _, row in edge_df.iterrows():
        G.add_edge(row['source'], row['target'], dir=edge_dir)
        G.write(f'{directory_path}/uncolored_graph.dot')

    # For each state, highlight the node and write to a separate dot file
    for _, row in state_df.iterrows():
        # Find the node corresponding to the state
        node = G.get_node(row['node_label'])
        node.attr['fillcolor'] = color_map[row['color']]
        node.attr['style'] = 'filled'
        G.write(f'{directory_path}/state_{row["state_id"]}_graph.dot')

    # Digest the node colored graph
    node_colored_graph = 'output/state_{}_graph.dot'.format(max(state_df["state_id"]))
    G = pgv.AGraph(node_colored_graph)

    # Get the color for each node
    node_color_dict = state_df.set_index('node_label')['color'].to_dict()

    # Adjusting edge colors based on node colors
    for _, row in edge_df.iterrows():
        source_node = row['source']
        target_node = row['target']
        source_col = node_color_dict[source_node]
        target_col = node_color_dict[target_node]
        edge = G.get_edge(source_node, target_node)
        # Check the colors and change the edge color accordingly
        if source_col == 'g' and target_col == 'r':
            edge.attr['color'] = '#00BB00' if mode == "game" else '#006ad1'
        elif source_col == 'r' and target_col == 'g':
            edge.attr['color'] = '#CC0000' if mode == "game" else '#cc8400'
        elif source_col == 'y' and target_col == 'y':
            edge.attr['color'] = '#AAAA00'
        else:
            edge.attr['color'] = '#b7b7b7'
            edge.attr['style'] = 'dashed'
        
    G.write(f'{directory_path}/colored_edge_graph.dot')

    import os

def generate_png_from_dot(directory='output'):
    """
    Generate PNG files from DOT files within a directory.

    :param directory: The directory path where DOT files are located.
    """

    # List all files in the specified directory
    files = os.listdir(directory)

    # Filter out the .dot files
    dot_files = [file for file in files if file.endswith('.dot')]

    for dot_file in dot_files:
        with open(f'{directory}/{dot_file}', 'r') as f:
            lines = f.readlines()

        with open(f'{directory}/{dot_file}', 'w') as f:
            f.writelines(lines)
        
        png_file = os.path.splitext(dot_file)[0] + '.png'  # Replace .dot extension with .png
        command = f'dot -Tpng {directory}/{dot_file} -o {directory}/{png_file}'
        os.system(command)
        
def display_image_slider(directory='output'):
    """
    Display an image slider widget to navigate through PNG images in the specified directory.

    :param directory: The directory path where PNG files are located.
    """
    
    image_files = os.listdir(directory)
    # Filter out only the files of interest
    state_files = [f for f in image_files if f.startswith('state_') and f.endswith('_graph.png')]
    # Sort these files based on the state_id
    state_files.sort(key=lambda f: float(re.search(r'(\d+(\.\d+)?)', f).group(1)))
    state_files = [directory + '/' + f for f in state_files]
    # Append the special files
    image_files = [directory + '/uncolored_graph.png'] + state_files + [directory + '/colored_edge_graph.png']

    # Create widgets
    image_slider = widgets.IntSlider(value=0, min=0, max=len(image_files)-1, step=1, description='Slide:')
    prev_button = widgets.Button(description='Previous')
    next_button = widgets.Button(description='Next')
    output = widgets.Output()

    # Define button click events
    def on_prev_button_clicked(b):
        if image_slider.value > 0:
            image_slider.value -= 1

    def on_next_button_clicked(b):
        if image_slider.value < len(image_files)-1:
            image_slider.value += 1

    prev_button.on_click(on_prev_button_clicked)
    next_button.on_click(on_next_button_clicked)

    # Define slider event
    def on_value_change(change):
        with output:
            clear_output(wait=True)
            img = mpimg.imread(image_files[image_slider.value])
            plt.imshow(img)
            plt.axis('off')
            plt.show()

    image_slider.observe(on_value_change, names='value')

    # Display widgets
    display(widgets.HBox([prev_button, next_button]))
    display(image_slider)
    display(output)

    # Initial image
    with output:
        img = mpimg.imread(image_files[0])
        plt.imshow(img)
        plt.axis('off')
        plt.show()