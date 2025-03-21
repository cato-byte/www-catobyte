import json
from datetime import datetime

class PostProcessor:
    def __init__(self, language="en"):
        """Initialize with a language setting restricted to 'es', 'en', or 'fr'."""
        allowed_languages = {"es", "en", "fr"}  # Set of allowed language codes

        if language not in allowed_languages:
            raise ValueError(f"Invalid language '{language}'. Allowed values are: 'es', 'en', 'fr'.")

        self.language = language  # Store the validated language

    def sort_posts(self, posts):
        """Sort posts by publication date (descending)."""
        return sorted(posts, key=lambda post: datetime.strptime(post['publication_date'], "%Y-%m-%d"), reverse=True)

    def get_adjacent_posts(self, posts, index):
        """Get 2 left and 2 right posts (circular)."""
        total_posts = len(posts)
        return [
            posts[(index - 2) % total_posts], 
            posts[(index - 1) % total_posts],
            posts[(index + 1) % total_posts], 
            posts[(index + 2) % total_posts]
        ]

    def build_section_from_adjacent_posts(self, adjacent_posts):
           # Definir el título según el idioma
        titles = {
            "es": "Otros posts",
            "fr": "Autres articles",
            "en": "Other posts"
        }
    
        section_title = titles.get(self.language, "Other posts")

        """Build an HTML section for adjacent posts."""
        return f"""<section class="old-posts-section">
        <h2>{section_title}</h2>
        <div class="old-posts">
            {''.join(f'''
            <div class="post">
                <a href="{post['post_url']}">
                    <img src="{post['title_image_url']}" alt="{post['title']}">
                    <p>{post['title']}</p>
                </a>
            </div>
            ''' for post in adjacent_posts)}
         </div>
        </section>"""

    def process_posts(self, posts):
        """Process posts and get neighborhoods."""
        sorted_posts = self.sort_posts(posts)
        post_neighborhoods = []

        for i, post in enumerate(sorted_posts):
            adjacent_posts = self.get_adjacent_posts(sorted_posts, i)
            other_post_section = self.build_section_from_adjacent_posts(adjacent_posts)
            post_neighborhoods.append({
                'post': post,
                'other_posts_section': other_post_section
            })

        return post_neighborhoods

    @staticmethod
    def read_posts_from_json(json_file_path):
        """Read posts from a JSON file."""
        with open(json_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)