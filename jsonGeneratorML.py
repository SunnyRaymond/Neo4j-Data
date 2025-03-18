import csv
import json

def safe_int(value):
    """Converts value to int if possible; returns None otherwise."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def load_nodes(csv_filename):
    nodes = []
    with open(csv_filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            node = {
                "address": row.get("address"),
                "name_tag": row.get("name_tag"),
                "label": row.get("label") if row.get("label") else "unknown"
            }
            nodes.append(node)
    print(f"Loaded {len(nodes)} nodes from {csv_filename}")
    return nodes

def load_edges(csv_filename):
    edges = []
    with open(csv_filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            edge = {
                "from": row.get("from"),
                "to": row.get("to"),
                "hash": row.get("hash"),
                "value": safe_int(row.get("value")),
                "timeStamp": safe_int(row.get("timeStamp")),
                "blockNumber": safe_int(row.get("blockNumber")),
                "tokenSymbol": row.get("tokenSymbol"),
                "contractAddress": row.get("contractAddress"),
                "isError": safe_int(row.get("isError")),
                "gasPrice": safe_int(row.get("gasPrice")),
                "gasUsed": safe_int(row.get("gasUsed"))
            }
            edges.append(edge)
    print(f"Loaded {len(edges)} edges from {csv_filename}")
    return edges

def main():
    nodes_csv = 'all-address.csv'  # Adjust path if necessary
    edges_csv = 'all-tx.csv'         # Adjust path if necessary
    output_json = 'moneylaundering.json'
    
    # Load nodes and edges from CSV files
    nodes = load_nodes(nodes_csv)
    edges = load_edges(edges_csv)
    
    # Combine data into one structure
    combined_data = {
        "nodes": nodes,
        "edges": edges
    }
    
    # Write out the JSON file
    with open(output_json, mode='w', encoding='utf-8') as json_file:
        json.dump(combined_data, json_file, indent=4)
    
    print(f"Combined JSON file generated at: {output_json}")

if __name__ == "__main__":
    main()
