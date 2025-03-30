import os
from create_other_posts_section import *
from metadata_utils import load_metadata_by_language
from config import TEMPLATES_DIR, PAGES_DIR, METADATA_FILE, LANGUAGES, CONTACT_EMAIL
from template_manager import TemplateManager


def read_template(template_name, language):
    """Lee el contenido de una plantilla desde el directorio de templates."""
    template_path = os.path.join(TEMPLATES_DIR, language, template_name)
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as template_file:
            return template_file.read()
    print(f"Warning: Template file {template_name} not found.")
    return ""


def insert_latest_posts_in_homepage(homepage_content, language):
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

    return homepage_content.replace('<!-- Dynamic content will be inserted here by Python script -->', latest_post_html)


def generate_misc_pages(language, template_manager):
    """Generates static pages for a specific language."""
    misc_pages = ['about.html', 'contact.html', 'home.html', 'privacy_policy.html', 'terms_of_service.html']

    for misc_page in misc_pages:
        localized_page = f"{language}/{misc_page}"  # E.g., en/home.html, es/home.html
        os.makedirs(os.path.join(PAGES_DIR, language), exist_ok=True)

        with open(os.path.join(PAGES_DIR, localized_page), 'w', encoding='utf-8') as html_file:
            # Use TemplateManager to write the header
            template_manager.write_header(html_file)

            # Load and process the page content
            page_content = template_manager.load_template(misc_page)
            if misc_page == 'home.html':
                page_content = insert_latest_posts_in_homepage(page_content, language)

            html_file.write(page_content)

            # Use TemplateManager to write the footer
            template_manager.write_footer(html_file, contact_email=CONTACT_EMAIL)


if __name__ == "__main__":
    for lang in LANGUAGES:
        # Initialize TemplateManager for the current language
        template_manager = TemplateManager(TEMPLATES_DIR, language=lang)
        generate_misc_pages(lang, template_manager)

    print("Pages successfully generated for all languages.")
