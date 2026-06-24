#!/usr/bin/env python3
import os
import sys
import shutil

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 bootstrap.py <NewProjectName> [DestinationDirectory]")
        print("Example: python3 bootstrap.py StoreBackend ./my-new-project")
        sys.exit(1)

    project_name = sys.argv[1]
    dest_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    # Target .gemini folder location
    gemini_dest = os.path.join(dest_dir, ".gemini")
    
    # Source template folder location (relative to this script)
    script_dir = os.path.dirname(os.path.realpath(__file__))
    
    print(f"Initializing Gemini rules and skills for project: '{project_name}'")
    print(f"Target directory: '{os.path.realpath(gemini_dest)}'")
    
    # 1. Create directories
    for sub in ["rules", "skills", "templates"]:
        os.makedirs(os.path.join(gemini_dest, sub), exist_ok=True)
        
    # 2. Walk and copy files while replacing placeholders
    for root, dirs, files in os.walk(script_dir):
        # Skip hidden files/folders and the script itself
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file == "bootstrap.py" or file == "bootstrap.sh" or file == "README.md":
                continue
                
            src_file_path = os.path.join(root, file)
            
            # Determine relative path from template root
            rel_path = os.path.relpath(src_file_path, script_dir)
            dest_file_path = os.path.join(gemini_dest, rel_path)
            
            # Create subdirectories in destination if they don't exist
            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
            
            # Read and replace placeholder
            try:
                with open(src_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Perform the placeholder replacements
                updated_content = content.replace("{ProjectName}", project_name)
                
                with open(dest_file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                    
            except Exception as e:
                print(f"Error copying {rel_path}: {e}")

    print("Success! Gemini rules and skills have been concretized and created successfully.")
    print("You can now copy the .gemini folder into the root of your new project workspace.")

if __name__ == "__main__":
    main()
