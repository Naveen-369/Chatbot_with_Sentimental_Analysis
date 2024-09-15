import os
import re

def find_imports(root_dir):
    imports = set()
    import_pattern = re.compile(r'^\s*(import|from)\s+([a-zA-Z0-9_]+)')

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        match = import_pattern.match(line)
                        if match:
                            imports.add(match.group(2))
    
    return imports

if __name__ == "__main__":
    root_directory = '.'  # Change this to your project root directory if needed
    deps = find_imports(root_directory)
    with open('requirements.txt', 'w') as f:
        for dep in deps:
            f.write(dep + '\n')
    print("Dependencies have been written to requirements.txt")