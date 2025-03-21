import subprocess
import os

# Define the scripts to run in the specified order
scripts = [
    "create_metadata.py",
    "raw_to_post.py",
    "create_other_post_section.py",
    "create_posts_archive.py",
    "create_default_img.py",
    "templates_to_pages.py"
]

def run_script(script_name):
    """Runs a Python script and logs the output."""
    print(f"Running {script_name}...")
    try:
        # Execute the script and wait for it to complete
        result = subprocess.run(["python3", script_name], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e.stderr}")

def main():
    # Change to the directory where scripts are located if needed
    script_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_directory)
    
    # Execute each script in the defined order
    for script in scripts:
        run_script(script)
    print("All scripts have been executed successfully!")

if __name__ == "__main__":
    main()