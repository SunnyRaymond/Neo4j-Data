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
    """
    nodes = []
    edges = []
    
    # Process nodes: ensure id is int and use the 'label' as name
    for node, data in G.nodes(data=True):
        node_id = data.get("id")
        if node_id is None:
            # If id attribute is missing, try to use the node key
            try:
                node_id = int(node)
            except ValueError:
                continue
        else:
            try:
                node_id = int(node_id)
            except ValueError:
                pass
        # Use 'label' as the node's name; if missing, default to an empty string.
        name = data.get("label", "")
        nodes.append({"id": node_id, "name": name})
    
    # Process edges: get integer source, target and weight ('value')
    for source, target, data in G.edges(data=True):
        # Retrieve the node id for source and target from the node attributes
        source_id = G.nodes[source].get("id", source)
        target_id = G.nodes[target].get("id", target)
        try:
            source_id = int(source_id)
        except ValueError:
            pass
        try:
            target_id = int(target_id)
        except ValueError:
            pass

        # Get the edge 'value', defaulting to 1 if not present
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
