import os
import json
from jinja2 import Environment, FileSystemLoader
from create_other_posts_section import *
from metadata_utils import load_metadata_by_language
from config import TEMPLATES_DIR, PAGES_DIR, METADATA_FILE, LANGUAGES, CONTACT_EMAIL, WHATSAPP_NUMBER, LINKEDIN_PROFILE, TEMPLATES_HTML_DIR, TEMPLATES_I18N_DIR
from template_manager import TemplateManager

def load_i18n(language):
    """Load the internationalization file for the given language."""
    i18n_file = os.path.join(TEMPLATES_I18N_DIR, f"{language}.json")
    with open(i18n_file, "r", encoding="utf-8") as file:
        return json.load(file)

def read_template(template_name, language):
    """Lee el contenido de una plantilla desde el directorio de templates."""
    template_path = os.path.join(TEMPLATES_DIR, language, template_name)
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as template_file:
            return template_file.read()
    print(f"Warning: Template file {template_name} not found.")
    return ""


def get_latest_posts_for_homepage( language):
    """Inserts the latest posts into the homepage based on the language."""
    posts = load_metadata_by_language(METADATA_FILE, language)
    post_processor = PostProcessor(language)
    sorted_posts = post_processor.sort_posts(posts)[:4]

    latest_post_html = "".join(
        f'''
        <div class="article">
            <a href="{post['post_url']}">
                <img src="{post['title_image_url']}" alt="{post['title_image_description']}">
                <h3>{post['title']}</h3>
            </a>
        </div>
        ''' for post in sorted_posts
    )

    return latest_post_html


def generate_pages():
    """Generate static pages for all languages."""
    templates = ["about.html", "contact.html", "services.html", "home.html", "privacy_policy.html", "terms_of_service.html"]

    for language in LANGUAGES:
        # Initialize TemplateManager for the current language
        template_manager = TemplateManager(language)

        # Render templates and store them in memory
        template_manager.render_templates(templates)

        # Write rendered templates to the output directory
        output_dir = os.path.join(PAGES_DIR, language)
        template_manager.write_templates_to_files(output_dir)

if __name__ == "__main__":
    generate_pages()
    print("Pages successfully generated.")
