import csv
import json

def load_edges_and_nodes(csv_filename):
    nodes_dict = {}  # key: node name, value: dict with keys "name" and "UuidFileMd5"
    edges = []
    
    with open(csv_filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Process edge attributes; keep all columns as they appear
            # Convert numeric fields when possible.
            try:
                index_val = int(row.get("Index", "").strip() or 0)
            except (ValueError, TypeError):
                index_val = None

            try:
                argc_val = int(row.get("Argc", "").strip() or 0)
            except (ValueError, TypeError):
                argc_val = None

            # We'll leave Argv, Return, Type, and EdgeNum as strings (or as-is)
            edge = {
                "Index": index_val,
                "UuidFileMd5": row.get("UuidFileMd5", "").strip(),
                "Caller": row.get("Caller", "").strip(),
                "Callee": row.get("Callee", "").strip(),
                "Argc": argc_val,
                "Argv": row.get("Argv", "").strip(),
                "Return": row.get("Return", "").strip(),
                "Type": row.get("Type", "").strip(),
                "EdgeNum": row.get("EdgeNum", "").strip()
            }
            edges.append(edge)
            
            # Update nodes dictionary for Caller and Callee.
            # For each node, if not seen before, store the node name and its UuidFileMd5 from the row.
            caller = edge["Caller"]
            callee = edge["Callee"]
            uuid_val = edge["UuidFileMd5"]
            if caller and caller not in nodes_dict:
                nodes_dict[caller] = {"name": caller, "UuidFileMd5": uuid_val}
            if callee and callee not in nodes_dict:
                nodes_dict[callee] = {"name": callee, "UuidFileMd5": uuid_val}
    
    # Now assign each node a unique id starting from 0.
    nodes = []
    for idx, node_name in enumerate(sorted(nodes_dict.keys())):
        node_data = nodes_dict[node_name]
        node_data["id"] = idx
        nodes.append(node_data)
    
    return nodes, edges

def main():
    csv_filename = "funcall.csv"  # Adjust path if necessary
    output_json = "funcall.json"
    
    nodes, edges = load_edges_and_nodes(csv_filename)
    print(f"Loaded {len(nodes)} unique nodes and {len(edges)} edges from {csv_filename}")
    
    combined_data = {
        "nodes": nodes,
        "edges": edges
    }
    
    with open(output_json, mode='w', encoding='utf-8') as json_file:
        json.dump(combined_data, json_file, indent=4)
    
    print(f"Generated JSON file '{output_json}' with {len(nodes)} nodes and {len(edges)} edges.")

if __name__ == "__main__":
    main()
