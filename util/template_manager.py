import os

class TemplateManager:
    
    def __init__(self, templates_dir, language=None):
        """
        Initialize the TemplateManager with the base templates directory and optional language.
        :param templates_dir: Base directory for templates.
        :param language: Language code (e.g., 'en', 'es') for localized templates.
        """
        self.templates_dir = templates_dir
        self.language = language
        self.templates = {}

    def _get_template_path(self, template_name):
        """
        Get the full path to a template file, considering the language if specified.
        :param template_name: Name of the template file (e.g., 'head.html').
        :return: Full path to the template file.
        """
        if self.language:
            localized_path = os.path.join(self.templates_dir, self.language, template_name)
            if os.path.exists(localized_path):
                return localized_path
        return os.path.join(self.templates_dir, template_name)

    def load_template(self, template_name):
        """
        Reads and caches the content of a template file.
        :param template_name: Name of the template file (e.g., 'head.html').
        :return: Content of the template file.
        """
        if template_name not in self.templates:
            template_path = self._get_template_path(template_name)
            if os.path.exists(template_path):
                with open(template_path, 'r', encoding='utf-8') as template_file:
                    self.templates[template_name] = template_file.read()
            else:
                print(f"Warning: Template file {template_name} not found.")
                self.templates[template_name] = ""
        return self.templates[template_name]

    def write_header(self, html_file):
        """
        Writes the common header to an HTML file.
        :param html_file: File object to write the header to.
        """
        head_content = self.load_template('head.html')
        header_content = self.load_template('header.html')
        navbar_content = self.load_template('navbar.html')

        html_file.write('<html>\n')
        html_file.write(head_content)
        html_file.write('<body>\n')
        html_file.write(header_content)
        html_file.write(navbar_content)
        html_file.write("<main>")

    def write_footer(self, html_file, contact_email=None):
        """
        Writes the common footer to an HTML file.
        :param html_file: File object to write the footer to.
        :param contact_email: Contact email to replace in the footer template.
        """
        footer_content = self.load_template('footer.html')
        if contact_email:
            footer_content = footer_content.replace('{{CONTACT_EMAIL}}', contact_email)
        html_file.write("</main>\n")
        html_file.write(footer_content)
        html_file.write('</body>\n</html>')
    
