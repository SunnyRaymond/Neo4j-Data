import json

def extract_unique_names(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    nodes = data.get("nodes", [])
    unique_names = set()
    for node in nodes:
        name = node.get("name")
        if name:
            unique_names.add(name)
    
    # Convert the set to a sorted list for consistency
    options = sorted(list(unique_names))
    return options

def main():
    json_file = "lesmiserables.json"  # Update the path if necessary
    options = extract_unique_names(json_file)
    
    # Print the array so you can copy it
    print(options)

if __name__ == "__main__":
    main()
