import subprocess
import os
import sys

def clean_build():
    """Clean the previous build files."""
    subprocess.run(['make', 'clean'], check=True)

def generate_rst_files():
    """Generate the reStructuredText files for the modules."""
    core_path = os.path.abspath('../core/qwak/')
    subprocess.run(['sphinx-apidoc', '-f', '-o', 'source/', core_path], check=True)

def build_html_docs():
    """Build the HTML documentation."""
    subprocess.run(['make', 'html'], check=True)

def check_docstring_changes():
    """Check for changes in the docstrings within the core folder of qwak."""
    core_path = os.path.abspath('../core/qwak/')
    subprocess.run(['git', 'diff', '--', core_path], check=True)

def main():
    """Main function to regenerate the documentation."""
    clean_build()
    generate_rst_files()
    build_html_docs()
    check_docstring_changes()
    print("Documentation generation complete.")

if __name__ == "__main__":
    main()
