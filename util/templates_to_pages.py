import os
from create_other_posts_section import *
from metadata_utils import load_metadata_by_language
from  config import TEMPLATES_DIR,PAGES_DIR,METADATA_FILE,LANGUAGES,CONTACT_EMAIL



def read_template(template_name,language):
    """Lee el contenido de una plantilla desde el directorio de templates."""
    template_path = os.path.join(TEMPLATES_DIR, language,template_name)
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as template_file:
            return template_file.read()
    print(f"Warning: Template file {template_name} not found.")
    return ""


def write_header(html_file,templates):
    print(templates['head.html'])
    """Escribe la cabecera común a todas las páginas."""
    html_file.write('<html>\n')
    html_file.write(templates['head.html'])
    html_file.write('<body>\n')
    html_file.write(templates['header.html'])
    html_file.write(templates['navbar.html'])
    html_file.write("<main>")

def write_footer(html_file,templates):
    """Escribe el pie de página común a todas las páginas."""
    html_file.write("</main>\n")
    html_file.write(templates['footer.html'].replace('{{CONTACT_EMAIL}}',CONTACT_EMAIL))
    html_file.write('</body>\n</html>')

def insert_latest_posts_in_homepage(homepage_content, language):
    """Inserta los últimos posts en la página de inicio según el idioma."""
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

def generate_misc_pages(language,templates):
    """Genera las páginas estáticas para un idioma específico."""
    misc_pages = ['about.html', 'contact.html', 'home.html', 'privacy_policy.html', 'terms_of_service.html']

    for misc_page in misc_pages:
        localized_page = f"{language}/{misc_page}"  # Ej: en/home.html, es/home.html
        os.makedirs(os.path.join(PAGES_DIR, language), exist_ok=True)

        with open(os.path.join(PAGES_DIR, localized_page), 'w', encoding='utf-8') as html_file:
            write_header(html_file,templates)
            page_content = read_template(misc_page,language)

            if misc_page == 'home.html':
                page_content = insert_latest_posts_in_homepage(page_content, language)

            html_file.write(page_content)
            write_footer(html_file,templates)

if __name__ == "__main__":
    for lang in LANGUAGES:
        templates_for_lang = {name: read_template(name,lang) for name in ['head.html', 'header.html', 'footer.html', 'navbar.html']}
        generate_misc_pages(lang,templates_for_lang)

    print("Páginas generadas exitosamente para todos los idiomas.")
