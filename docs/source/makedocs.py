import subprocess
import os

# Define the modules and the source directory
modules = ['../core/qwak/', '../core/utils/']
source_dir = 'source/'

# Ensure the source directory exists
os.makedirs(source_dir, exist_ok=True)

# Initialize or clear the main 'modules.rst' file
modules_rst_path = os.path.join(source_dir, 'modules.rst')
with open(modules_rst_path, 'w') as f:
    f.write('Modules\n=======\n\n.. toctree::\n   :maxdepth: 4\n\n')

# Function to append module documentation to 'modules.rst'
def append_to_modules_rst(module_name):
    with open(modules_rst_path, 'a') as f:
        f.write(f'   {module_name}/modules\n')

# Function to run sphinx-apidoc on a module
def generate_module_docs(module_path):
    # Determine the module name from the path
    module_name = os.path.basename(os.path.normpath(module_path))
    # Run sphinx-apidoc for the module
    subprocess.run(['sphinx-apidoc', '-f', '-o', source_dir, module_path], check=True)
    # Append the module's entry to 'modules.rst'
    append_to_modules_rst(module_name)

# Generate documentation for each module
for module in modules:
    generate_module_docs(module)

print("Documentation generation complete.")
