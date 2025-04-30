import os
import textwrap
import re
from datetime import datetime
from create_other_posts_section import PostProcessor
from metadata_utils import load_metadata_by_language
from datetime import datetime
from config import RAW_DIR,POSTS_DIR,TEMPLATES_DIR,METADATA_FILE,LANGUAGES
from template_manager import TemplateManager



# Function to add the correct suffix for the day
def get_day_with_suffix(day, lang="en"):
    if lang == "en":
        if 11 <= day <= 13:  # Special case for 11th, 12th, 13th
            return f"{day}th"
        elif day % 10 == 1:
            return f"{day}st"
        elif day % 10 == 2:
            return f"{day}nd"
        elif day % 10 == 3:
            return f"{day}rd"
        else:
            return f"{day}th"

    elif lang in ["es", "fr"]:  
        return str(day)  # In Spanish and French, days do not have suffixes

# Function to format the date correctly for each language
def format_date(date_str, lang="en"):
    # Parse the date from the string
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')

    # Extract day, month, and year
    day_with_suffix = get_day_with_suffix(date_obj.day, lang)

    # Define month names in different languages
    months = {
        "en": {
            "January": "January", "February": "February", "March": "March", "April": "April",
            "May": "May", "June": "June", "July": "July", "August": "August",
            "September": "September", "October": "October", "November": "November", "December": "December"
        },
        "es": {
            "January": "enero", "February": "febrero", "March": "marzo", "April": "abril",
            "May": "mayo", "June": "junio", "July": "julio", "August": "agosto",
            "September": "septiembre", "October": "octubre", "November": "noviembre", "December": "diciembre"
        },
        "fr": {
            "January": "janvier", "February": "février", "March": "mars", "April": "avril",
            "May": "mai", "June": "juin", "July": "juillet", "August": "août",
            "September": "septembre", "October": "octobre", "November": "novembre", "December": "décembre"
        }
    }

    # Get the full month name in English and translate it
    month_en = date_obj.strftime('%B')
    month_translated = months[lang].get(month_en, month_en)

    year = date_obj.year

    # Return the formatted string
    if lang == "en":
        return f"{day_with_suffix} of {month_translated} {year}"
    elif lang == "es":
        return f"{day_with_suffix} de {month_translated} de {year}"
    elif lang == "fr":
        return f"{day_with_suffix} {month_translated} {year}"



def read_template(template_name, templates_dir):
    """Reads the content of a template file."""
    template_path = os.path.join(templates_dir, template_name)
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as template_file:
            return template_file.read()
    else:
        print(f"Warning: Template file {template_name} not found.")
        return ""


def markdown_table_to_html(table_lines):
    """Converts a list of markdown table lines to styled HTML."""
    headers = table_lines[0].split('|')[1:-1]  # Skip the outer '|'
    data_rows = [line.split('|')[1:-1] for line in table_lines[2:]]  # Ignore header separator

    # Add the table class for consistent styling
    html = '<table class="styled-table">\n  <thead>\n    <tr>\n'
    for header in headers:
        html += f'      <th>{header.strip()}</th>\n'
    html += '    </tr>\n  </thead>\n  <tbody>\n'
    for row in data_rows:
        html += '    <tr>\n'
        for cell in row:
            html += f'      <td>{cell.strip()}</td>\n'
        html += '    </tr>\n'
    html += '  </tbody>\n</table>'

    return html

def markdown_to_html(line,is_title_image):
    """Converts markdown syntax to HTML."""

    # Convert headings
    line = re.sub(r'^######\s*(.*)', r'<h6>\1</h6>', line)  # ### for <h5>
    line = re.sub(r'^#####\s*(.*)', r'<h5>\1</h5>', line)  # ### for <h5>
    line = re.sub(r'^####\s*(.*)', r'<h4>\1</h4>', line)  # ### for <h5>
    line = re.sub(r'^###\s*(.*)', r'<h3>\1</h3>', line)  # ### for <h3>
    line = re.sub(r'^##\s*(.*)', r'<h2>\1</h2>', line)  # ## for <h2>
    



    # Convert images ![alt](src)
    if is_title_image:
        line = re.sub(r'!\[(.*?)\]\((.*?)\)',  r"""          <div class="image-container">
                <img src="\2" alt="\1" class="responsive-title-image">
                <h6 class="image-source"> \1 </h6>
            </div>""", line)
    else:
        line = re.sub(r'!\[(.*?)\]\((.*?)\)', r"""          <div class="image-container">
                <img src="\2" alt="\1" class="responsive-image">
                <h6 class="image-source"> \1 </h6>
            </div>""", line)

    return line

def fill_markdown_links(line):
    # Convert bold (**) and italic (*)
    line = re.sub(r'^\*\*(.*?)\*\*', r'<b>\1</b>', line)  # ** for bold
    line = re.sub(r'^\*(.*?)\*', r'<em>\1</em>', line)  # * for italic
    # Replace the Markdown link with an HTML anchor tag
    line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', line)

    return line

def convert_code_block_to_html(code_lines, language):
    """
    Converts a code block to an HTML string with appropriate CSS classes for Prism.js.
    
    :param code_lines: List of code lines in the block.
    :param language: Programming language of the code block.
    :return: HTML string for the code block.
    """
    # Use the appropriate language class; default to plaintext if not specified
    language_class = f"language-{language}" if language else "language-text"
    
    # Join code lines and escape HTML special characters
    code_content = "\n".join(code_lines)
    code_content = (
        code_content.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    
    # Return the HTML structure compatible with Prism.js plugins (e.g., toolbar)
    return (
        f'<div class="code-toolbar">\n'
        f'  <pre>\n'
        f'    <code class="{language_class} line-numbers">{code_content}</code>\n'
        f'  </pre>\n'
        f'</div>\n'
    )

def txt_to_html(raw_dir, posts_dir, templates_dir, posts, lang):
    if os.path.exists(posts_dir):
        # Clear existing HTML files from posts directory
        for filename in os.listdir(posts_dir):
            if filename.endswith('.html'):
                os.remove(os.path.join(posts_dir, filename))
        print("All existing HTML files in the posts directory have been deleted.")
    else:
        os.makedirs(posts_dir)  # Create the posts directory if it doesn't exist

    # Initialize the TemplateManager
    template_manager = TemplateManager(language=lang)

    # Circular relation between the posts for other posts section
    post_processor = PostProcessor(language=lang)
    post_neighborhoods = post_processor.process_posts(posts)

    for post_neighborhood in post_neighborhoods:
        post = post_neighborhood['post']
        filename = post['file_name']
        if filename.endswith(".md"):  # Use .md extension for markdown files
            md_file_path = os.path.join(raw_dir, filename)

            # Change the file extension from .md to .html
            html_filename = os.path.splitext(os.path.basename(filename))[0] + ".html"
            html_file_path = os.path.join(posts_dir, html_filename)
            print(raw_dir, posts_dir, templates_dir, html_filename, html_file_path)

            # Check if the file has already been processed
            if os.path.exists(html_file_path):
                print(f"{html_filename} already exists. Skipping...")
                continue

            # Read the .md file and write the corresponding .html file
            with open(md_file_path, 'r', encoding='utf-8') as md_file, open(html_file_path, 'w', encoding='utf-8') as html_file:
                # Write the header using TemplateManager
                template_manager.write_header(html_file)

                # Write the main content
                html_file.write("""<main>\n<div class="vertical-body-container">\n""")
                is_title_image = False
                table_lines = []
                is_parsing_table = False
                code_lines = []
                is_code_block = False
                code_language = ""

                for line in md_file:
                    stripped_line = line.strip()

                    # Detect the TITLE_IMAGE comment
                    if stripped_line == "<!-- TITLE_IMAGE -->":
                        is_title_image = True
                        continue

                    # Ignore empty lines
                    if not stripped_line:
                        continue

                    # Detect the start of a code block
                    if stripped_line.startswith("```"):
                        if not is_code_block:  # Beginning of a new code block
                            is_code_block = True
                            code_language = stripped_line[3:]  # Capture the language after ```
                        else:  # End of the current code block
                            is_code_block = False
                            # Convert the collected code lines to an HTML block
                            html_block = convert_code_block_to_html(code_lines, code_language)
                            html_file.write(html_block)  # Write the HTML block to the file
                            # Reset for the next potential block
                            code_language = None
                            code_lines = []
                        continue

                    # Collect code lines if inside a code block
                    if is_code_block:
                        code_lines.append(stripped_line)
                        continue

                    # Check if the line is part of a markdown table
                    if re.match(r'^\|.*\|$', stripped_line) and not is_parsing_table:
                        is_parsing_table = True
                        table_lines.append(stripped_line)
                        continue

                    if is_parsing_table:
                        if re.match(r'^\|[-\s|]+\|$', stripped_line):
                            table_lines.append(stripped_line)
                        elif re.match(r'^\|.*\|$', stripped_line):
                            table_lines.append(stripped_line)
                        else:
                            html_file.write(markdown_table_to_html(table_lines))
                            table_lines = []
                            is_parsing_table = False

                    if not is_parsing_table:
                        # Convert the markdown line to HTML
                        html_line = markdown_to_html(stripped_line, is_title_image)

                        # Reset the title image flag after processing the image
                        if is_title_image:
                            is_title_image = False

                        if re.search(r'\{\{PUBLISH_DATE\}\}', html_line):
                            html_line = html_line.replace("{{PUBLISH_DATE}}", format_date(post['publication_date'], lang=lang))

                        if stripped_line == html_line:
                            stripped_line = fill_markdown_links(stripped_line)
                            # Split into wrapped lines less than 80 characters
                            wrapped_lines = textwrap.wrap(stripped_line, width=80)

                            # Embed each wrapped line in <p> tags and write to the HTML file
                            html_file.write(f'          <p>\n')
                            for wrapped_line in wrapped_lines:
                                html_file.write(f'              {wrapped_line}\n')
                            html_file.write(f'          </p>\n')
                        else:
                            # Write the processed HTML line
                            html_file.write(f'          {html_line}\n')

                        if is_parsing_table and table_lines:
                            html_file.write(markdown_table_to_html(table_lines))

                # Write the end of the main content
                html_file.write("</div>\n</main>\n")
                html_file.write(post_neighborhood['other_posts_section'])

                # Write the footer using TemplateManager
                template_manager.write_footer(html_file)

            print(f"Processed {filename} to {html_file_path}")


def main():
    """Procesa todos los idiomas y genera los archivos HTML correspondientes."""
    if not LANGUAGES:
        raise ValueError("LANGUAGES list is empty. Please define at least one language.")

    for lang in LANGUAGES:
        if not lang:
            print("Warning: Skipping an empty language entry.")
            continue

        RAW_DIR_LANG = os.path.join(RAW_DIR, lang)
        POSTS_DIR_LANG = os.path.join(POSTS_DIR, lang)
        TEMPLATES_DIR_LANG = os.path.join(TEMPLATES_DIR, lang)

        lang_posts = load_metadata_by_language(METADATA_FILE, lang)
        txt_to_html(RAW_DIR_LANG, POSTS_DIR_LANG, TEMPLATES_DIR_LANG, lang_posts, lang)


# Ejecuta el método principal
if __name__ == "__main__":
    main()