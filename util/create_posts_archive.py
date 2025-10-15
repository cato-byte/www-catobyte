from pathlib import Path
import os
from datetime import datetime
from metadata_utils import load_metadata_by_language
from config import WEB_DIR, LANGUAGES
from template_manager import TemplateManager


def get_paths(language):
    """Returns the relevant paths for a given language."""
    return {
        'pages_dir': os.path.join(WEB_DIR, 'pages', language),
        'metadata_file': os.path.join(WEB_DIR, 'metadata', 'posts_metadata.json'),
        'output_html': os.path.join(WEB_DIR, 'pages', language, 'archive.html'),
    }


def parse_date(post):
    """Parses the publication_date string into a datetime object."""
    return datetime.strptime(post['publication_date'], '%Y-%m-%d')


def generate_archive(language):
    """Generates the archive HTML for a specific language."""
    paths = get_paths(language)

    # Ensure output directory exists
    os.makedirs(paths['pages_dir'], exist_ok=True)

    # Read metadata file
    if not os.path.exists(paths['metadata_file']):
        print(f"Warning: Metadata file not found. Skipping.")
        return

    posts = load_metadata_by_language(paths['metadata_file'], language)

    # Sort posts by publication date (newest first)
    sorted_posts = sorted(posts, key=parse_date, reverse=True)

    # Initialize TemplateManager
    template_manager = TemplateManager(language=language)

    # Write HTML file
    with open(paths['output_html'], 'w', encoding='utf-8') as html_file:
        # Write the header using TemplateManager
        template_manager.write_header(html_file)

        # Write the main content main tag added by template manager
        html_file.write(f"""
                        
            <h2> Blog Archive ({language.upper()}) </h2>
            <div class="archive-container">
        """)

        for post in sorted_posts:
            html_file.write(f'''
                <div class="post-item">
                    <a href="{post['post_url']}">
                        <img src="{post['title_image_url']}" alt="{post['title']} image" width="80" height="80" style="float:left; margin-right:10px;">
                        <span style="display:inline-block; vertical-align:middle;">{post['title']}</span>
                    </a>
                    <span class="publication-date" style="float:right;">{post['publication_date']}</span>
                </div>
                <hr>
            ''')

        html_file.write("""
            </div>
        </main>
        """)

        # Write the footer using TemplateManager
        template_manager.write_footer(html_file)

    print(f"HTML archive generated: {paths['output_html']}")


def generate_posts_all_languages():
    # Process all languages
    for lang in LANGUAGES:
        generate_archive(lang)


if __name__ == "__main__":
    generate_posts_all_languages()
