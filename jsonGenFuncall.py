import csv
import json

def load_edges_and_nodes(csv_filename):
    nodes_set = set()
    edges = []
    
    with open(csv_filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Get node names from Caller and Callee columns
            caller = row.get("Caller")
            callee = row.get("Callee")
            if caller:
                nodes_set.add(caller)
            if callee:
                nodes_set.add(callee)
            
            # Process edge attributes: ignore UuidFileMd5
            try:
                index_val = int(row.get("Index"))
            except (ValueError, TypeError):
                index_val = None
            
            try:
                argc_val = int(row.get("Argc"))
            except (ValueError, TypeError):
                argc_val = None

            # Argv and Return remain as strings (default to empty string if missing)
            edge = {
                "Caller": caller,
                "Callee": callee,
                "Index": index_val,
                "Argc": argc_val,
                "Argv": row.get("Argv", ""),
                "Return": row.get("Return", "")
            }
            edges.append(edge)
    
    # Create node objects with unique names
    nodes = [{"name": name} for name in sorted(nodes_set)]
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
