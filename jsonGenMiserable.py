import networkx as nx
import json

def load_gml(gml_filename):
    """
    Load the GML file into a NetworkX graph.
    """
    G = nx.read_gml(gml_filename)
    return G

def convert_graph_to_json(G):
    """
    Convert the NetworkX graph to a JSON structure with:
      - nodes: { "id": int, "name": string }
      - edges: { "source": int, "target": int, "value": int }
    This function builds a mapping for node keys to new integer ids.
    """
    nodes = []
    edges = []
    
    # Create a mapping from each node key to a new integer id.
    node_id_mapping = {}
    next_id = 0
    for node, data in G.nodes(data=True):
        # If the node data has an 'id' that can be converted, use it.
        if "id" in data:
            try:
                int_id = int(data["id"])
            except ValueError:
                int_id = next_id
                next_id += 1
        else:
            int_id = next_id
            next_id += 1
        
        node_id_mapping[node] = int_id
        # Use the 'label' attribute as the name; if missing, use the node key.
        name = data.get("label", str(node))
        nodes.append({"id": int_id, "name": name})
    
    # Process edges: use the mapping to assign integer ids to source and target.
    for source, target, data in G.edges(data=True):
        source_id = node_id_mapping[source]
        target_id = node_id_mapping[target]
        # Get the edge 'value'; default to 1 if not present.
        edge_value = data.get("value", 1)
        try:
            edge_value = int(edge_value)
        except ValueError:
            edge_value = 1
        
        edges.append({"source": source_id, "target": target_id, "value": edge_value})
    
    return {"nodes": nodes, "edges": edges}

def main():
    gml_filename = "lesmiserables.gml"      # Update path if necessary
    output_json_filename = "lesmiserables.json"
    
    print("Loading GML file...")
    G = load_gml(gml_filename)
    print(f"Loaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    
    # Convert graph to JSON structure
    combined_data = convert_graph_to_json(G)
    print(f"Converted to JSON with {len(combined_data['nodes'])} nodes and {len(combined_data['edges'])} edges")
    
    # Write the combined data to a JSON file
    with open(output_json_filename, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, indent=4)
    
    print(f"JSON data written to {output_json_filename}")

if __name__ == "__main__":
    main()
