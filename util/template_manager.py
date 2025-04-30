import os
import json
from jinja2 import Environment, FileSystemLoader
from config import TEMPLATES_HTML_DIR, TEMPLATES_I18N_DIR, METADATA_FILE, CONTACT_EMAIL, WHATSAPP_NUMBER, LINKEDIN_PROFILE

class TemplateManager:
    def __init__(self, language):
        """
        Initialize the TemplateManager with the base templates directory and language.
        :param language: Language code (e.g., 'en', 'es', 'fr').
        """
        if not language:
            raise ValueError("Language cannot be empty. Please provide a valid language code.")
        
        self.language = language
        self.templates_dir = TEMPLATES_HTML_DIR
        self.i18n_dir = TEMPLATES_I18N_DIR
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))
        self.i18n_data = self._load_i18n_data()
        self.rendered_templates = {}  # Store rendered templates for later access
        self.context = self._generate_context()  # Preload the context

    def _load_i18n_data(self):
        """
        Load the internationalization data for the given language.
        :return: A dictionary containing the i18n data.
        """
        i18n_file = os.path.join(self.i18n_dir, f"{self.language}.json")
        if os.path.exists(i18n_file):
            with open(i18n_file, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            print(f"Warning: i18n file for language '{self.language}' not found.")
            return {}

    def _generate_context(self):
        """
        Generate the context dictionary for rendering templates.
        :return: A dictionary containing the context data.
        """
        return {
            "i18n": self.i18n_data,
            "CONTACT_EMAIL": CONTACT_EMAIL,
            "WHATSAPP_NUMBER": WHATSAPP_NUMBER,
            "LINKEDIN_PROFILE": LINKEDIN_PROFILE,
            "LATEST_ARTICLES": self.get_latest_posts_for_homepage(),
        }

    def get_latest_posts_for_homepage(self):
        """
        Generate the latest posts section for the homepage.
        :return: HTML string for the latest posts section.
        """
        from metadata_utils import load_metadata_by_language
        from create_other_posts_section import PostProcessor

        posts = load_metadata_by_language(METADATA_FILE, self.language)
        post_processor = PostProcessor(self.language)
        sorted_posts = post_processor.sort_posts(posts)[:4]

        return "".join(
            f'''
            <div class="article">
                <a href="{post['post_url']}">
                    <img src="{post['title_image_url']}" alt="{post['title_image_description']}">
                    <h3>{post['title']}</h3>
                </a>
            </div>
            ''' for post in sorted_posts
        )

    def render_templates(self, templates):
        """
        Render all templates for the given language and store them in memory.
        :param templates: List of template filenames to render.
        """
        for template_name in templates:
            template = self.env.get_template(template_name)
            self.rendered_templates[template_name] = template.render(self.context)

    def write_templates_to_files(self, output_dir):
        """
        Write the rendered templates to the output directory.
        :param output_dir: Directory where the rendered templates will be saved.
        """
        os.makedirs(output_dir, exist_ok=True)

        for template_name, rendered_content in self.rendered_templates.items():
            output_path = os.path.join(output_dir, template_name)
            with open(output_path, "w", encoding="utf-8") as html_file:
                # Write header
                self.write_header(html_file)

                # Write the rendered content
                html_file.write(rendered_content)

                # Write footer
                self.write_footer(html_file)

    def write_header(self, html_file):
        """
        Writes the common header to an HTML file.
        :param html_file: File object to write the header to.
        """
        head_content = self.env.get_template('head.html').render(self.context)
        header_content = self.env.get_template('header.html').render(self.context)
        navbar_content = self.env.get_template('navbar.html').render(self.context)

        html_file.write('<html>\n')
        html_file.write(head_content)
        html_file.write('<body>\n')
        html_file.write(header_content)
        html_file.write(navbar_content)
        html_file.write("<main>")

    def write_footer(self, html_file):
        """
        Writes the common footer to an HTML file.
        :param html_file: File object to write the footer to.
        """
        footer_content = self.env.get_template('footer.html').render(self.context)
        html_file.write("</main>\n")
        html_file.write(footer_content)
        html_file.write('</body>\n</html>')


