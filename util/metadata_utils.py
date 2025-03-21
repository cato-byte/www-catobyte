import json

def load_metadata_by_language(metadata_file, language):
    # Read the JSON file
    with open(metadata_file, 'r') as file:
        posts = json.load(file)
    
    # Initialize a list to hold the filtered data
    filtered_posts = []

    # Loop through the metadata and extract Language and shared data
    for post in posts:
        # Check if the 'languages' key exists and is a dictionary
        if 'languages' in post and isinstance(post['languages'], dict):
            # Extract Language info safely using .get() to avoid key errors
            lang_data = post['languages'].get(language, None)

            # If lang_data is None or empty, skip the post
            if lang_data is None:
                print(f"Skipping post with ID {post['post_id']} as language '{language}' is not available.")
                continue

            # Extract shared data
            shared_data = { 
                'post_id': post['post_id'], 
                'creation_date': post['creation_date'],
                'publication_date': post['publication_date'],
                'title_image_url': post['title_image_url']
            }
            
            # Combine shared data with Language-specific information
            lang_post_data = {**shared_data, **lang_data}
            
            # Add the filtered post to the list
            filtered_posts.append(lang_post_data)
        else:
            print(f"Skipping post with ID {post['post_id']} due to missing 'languages' data.")
    
    return filtered_posts