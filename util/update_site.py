import subprocess
import os
import create_metadata,  create_posts_archive, create_default_img, templates_to_pages, raw_to_post




def update_website():
    """Runs a Python script and logs the output."""
    try:
        create_metadata.process_markdown_files()  
        create_posts_archive.generate_posts_all_languages()
        create_default_img.create_default_images()
        templates_to_pages.generate_pages()
        raw_to_post.markdowns_to_posts()
    except Exception as e:
        print(f"Error running {script_name}: {e.stderr}")

if __name__ == "__main__":
    update_website()