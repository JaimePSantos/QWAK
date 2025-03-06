import ast
import os

def extract_docstrings(filepath):
    with open(filepath, "r") as file:
        tree = ast.parse(file.read())
    
    docstrings = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) or isinstance(node, ast.FunctionDef):
            docstring = ast.get_docstring(node)
            if docstring:
                docstrings[node.name] = docstring
    return docstrings

def generate_rst(docstrings, output_filepath):
    with open(output_filepath, "w") as file:
        for name, docstring in docstrings.items():
            file.write(f"{name}\n{'=' * len(name)}\n\n")
            file.write(f"{docstring}\n\n")

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".py"):
                input_filepath = os.path.join(root, file)
                relative_path = os.path.relpath(input_filepath, input_dir)
                output_filepath = os.path.join(output_dir, relative_path).replace(".py", ".rst")
                
                docstrings = extract_docstrings(input_filepath)
                generate_rst(docstrings, output_filepath)

def process_all_directories(core_dir, docs_source_dir):
    for item in os.listdir(core_dir):
        item_path = os.path.join(core_dir, item)
        if os.path.isdir(item_path):
            output_dir = os.path.join(docs_source_dir, item)
            process_directory(item_path, output_dir)

if __name__ == "__main__":
    core_dir = r"c:\Users\jaime\Documents\GitHub\QWAK\core"
    docs_source_dir = r"c:\Users\jaime\Documents\GitHub\QWAK\docs\source"
    
    process_all_directories(core_dir, docs_source_dir)
