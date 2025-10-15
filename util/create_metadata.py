import os
import json
import re
from datetime import datetime
from config import METADATA_FILE,RELATIVE_POST_DIR,RAW_DIR


# Relative paths for URLs
#images_folder = "../../images"
#posts_folder = "../../post"

# Get today's date
today_date = datetime.now().strftime("%Y-%m-%d")

def detect_language(filename):
    """ Detect language based on folder structure. """
    if "/en/" in filename:
        return "en"
    elif "/es/" in filename:
        return "es"
    elif "/fr/" in filename:
        return "fr"
    return None

def extract_post_metadata(file_path):
    """ Extract title, image, and description from a markdown file. """
    title, title_image_url, title_image_description = "", "", ""
    title_found, is_title_image = False, False

    with open(file_path, "r", encoding="utf-8") as md_file:
        for line in md_file:
            
            stripped_line = line.strip()

            if re.match(r"^##\s*(.*)", stripped_line) and not title_found:
                title = re.sub(r"^##\s*(.*)", r"\1", stripped_line)
                title_found = True
                continue

            if stripped_line == "<!-- TITLE_IMAGE -->":
                is_title_image = True
                continue

            if is_title_image and re.match(r"!\[.*\]\(.*\)", stripped_line):
                print(stripped_line)
                title_image_url = re.sub(r"!\[(.*?)\]\((.*?)\)", r"\2", stripped_line)
                print(title_image_url)
                title_image_description = re.sub(r"!\[(.*?)\]\((.*?)\)", r"\1", stripped_line)
                break

    return title, title_image_url, title_image_description

def update_metadata(new_posts_data, destination_file):
    """ Merge new posts with existing metadata while preserving creation dates. """
    existing_posts = {}

    # Load existing metadata if it exists
    if os.path.exists(destination_file):
        with open(destination_file, "r", encoding="utf-8") as f:
            for post in json.load(f):
                existing_posts[post["post_id"]] = post

    for new_post_data in new_posts_data:
        post_id = new_post_data["post_id"]

        if post_id in existing_posts:
            # Preserve existing creation date
            new_post_data["creation_date"] = existing_posts[post_id]["creation_date"]
            new_post_data["publication_date"] = existing_posts[post_id]["publication_date"]
            # Merge data
            existing_posts[post_id].update(new_post_data)
        else:
            # Add new post
            existing_posts[post_id] = new_post_data

    # Save updated metadata
    with open(destination_file, "w", encoding="utf-8") as f:
        json.dump(list(existing_posts.values()), f, indent=4, ensure_ascii=False)

def process_markdown_files():
    
    # Process all markdown files and categorize them by language
    posts_metadata = {}

    for root, _, files in os.walk(RAW_DIR):
        for filename in files:
            if filename.endswith(".md"):
                file_path = os.path.join(root, filename)
                language = detect_language(os.path.join(root, filename))
                
                if not language:
                    continue  # Skip files that don't fit language folders

                post_id = os.path.splitext(filename)[0]  # Remove .md extension
                title, img_url, img_desc = extract_post_metadata(file_path)

                if post_id not in posts_metadata:
                    posts_metadata[post_id] = {
                        "post_id": post_id,
                        "languages": {},
                        "creation_date": today_date,
                        "publication_date": today_date,
                        "title_image_url": img_url,
                    }

                posts_metadata[post_id]["languages"][language] = {
                    "file_name": filename,
                    "title": title,
                    "post_url": f"{RELATIVE_POST_DIR}/{language}/{post_id}.html",
                    "title_image_description": img_desc,
                }

#    Convert dictionary to list format for JSON storage
    update_metadata(list(posts_metadata.values()), METADATA_FILE)

if __name__ == "__main__":
    process_markdown_files()
