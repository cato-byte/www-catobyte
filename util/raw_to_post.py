import os
import textwrap
import re
from datetime import datetime
from create_other_posts_section import PostProcessor
from metadata_utils import load_metadata_by_language
from datetime import datetime
from config import RAW_DIR,POSTS_DIR,TEMPLATES_DIR,METADATA_FILE,LANGUAGES
from template_manager import TemplateManager




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
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    day_with_suffix = get_day_with_suffix(date_obj.day, lang)
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

def prepare_output_directory(posts_dir):
    """Ensure posts_dir exists and remove old HTML files."""
    if os.path.exists(posts_dir):
        for filename in os.listdir(posts_dir):
            if filename.endswith('.html'):
                os.remove(os.path.join(posts_dir, filename))
        print("All existing HTML files in the posts directory have been deleted.")
    else:
        os.makedirs(posts_dir)

def unordered_list_to_html(unordered_list_lines):
    """Convert a list of unordered list items to HTML."""
    html = '          <ul>\n'
    for item in unordered_list_lines:
        html += f'              <li>{item}</li>\n'
    html += '          </ul>\n'
    return html   

def handle_code_block(stripped_line, is_code_block, code_language, code_lines):
    if stripped_line.startswith("```"):
        if not is_code_block:
            return None,True, stripped_line[3:]
        else:
            html_block = convert_code_block_to_html(code_lines, code_language)
            code_lines.clear()
            return html_block, False, ""
    elif is_code_block:
            code_lines.append(stripped_line)    
    return None, is_code_block, code_language

def handle_table_lines(line, is_parsing_table, table_lines):
    """Manage table parsing and write HTML when table ends."""
    if re.match(r'^\|.*\|$', line) and not is_parsing_table:
        table_lines.append(line)
        return None,True

    if is_parsing_table:
        if re.match(r'^\|[-\s|]+\|$', line) or re.match(r'^\|.*\|$', line):
            table_lines.append(line)
            return None,True
        else:
            html_table = markdown_table_to_html(table_lines)
            table_lines.clear()
            return html_table,False
    return None,False

def handle_unordered_list(line, is_unordered_list, unordered_list_lines):
    """Manage unordered list parsing and write HTML when list ends."""
    if line.startswith('- '):
        unordered_list_lines.append(line[2:].strip())
        return None,True
    elif is_unordered_list:
        html_block = unordered_list_to_html(unordered_list_lines)
        unordered_list_lines.clear()
        return html_block, False
    return None, False

def build_html_line( stripped_line, post, lang, is_title_image):
    """Convert markdown line to HTML and write to file."""
    html_line = markdown_to_html(stripped_line, is_title_image)

    if re.search(r'\{\{PUBLISH_DATE\}\}', html_line):
        html_line = html_line.replace("{{PUBLISH_DATE}}", format_date(post['publication_date'], lang=lang))

    if stripped_line == html_line:
        stripped_line = fill_markdown_links(stripped_line)
        wrapped = textwrap.wrap(stripped_line, width=80)
        paragraph = '          <p>\n'
        for w in wrapped:
            paragraph += f'              {w}\n'
        paragraph += '          </p>\n'
        return paragraph
    else:
        return f'          {html_line}\n'
    
def flush_pending_blocks(html_file,
                         table_lines, is_parsing_table,
                         unordered_list_lines, is_unordered_list,
                         code_lines, is_code_block, code_language):
    
    if is_unordered_list and unordered_list_lines:
        html_file.write(unordered_list_to_html(unordered_list_lines))

    if is_parsing_table and table_lines:
        html_file.write(markdown_table_to_html(table_lines))


    if is_code_block and code_lines:
        html_file.write(convert_code_block_to_html(code_lines, code_language))


    if not any([is_code_block, is_parsing_table, is_unordered_list]):
        html_file.flush()

def parse_markdown_lines(md_file, html_file, post, lang):
    is_title_image = False
    table_lines = []
    is_parsing_table = False
    code_lines = []
    is_code_block = False
    code_language = ""
    is_unordered_list = False
    unordered_list_lines = []

    for line in md_file:
        stripped_line = line.strip()

        # Detect the TITLE_IMAGE comment
        if stripped_line == "<!-- TITLE_IMAGE -->":
            is_title_image = True
            continue

        # Ignore empty lines
        if not stripped_line:
            continue
        
        #TODO: Refactor handlers to reduce repetition and  avoid order issues

        # Handle unordered lists
        list_html, is_unordered_list = handle_unordered_list(
            stripped_line, is_unordered_list, unordered_list_lines
        )
        if is_unordered_list:
            continue
        if list_html is not None:
            html_file.write(list_html)

        # Handle tables
        table_html, is_parsing_table = handle_table_lines(stripped_line, is_parsing_table, table_lines)
        if is_parsing_table:
            continue
        if table_html is not None:
            html_file.write(table_html)

        # Handle code blocks
        code_block_html, is_code_block, code_language = handle_code_block(
            stripped_line, is_code_block, code_language, code_lines
        )
        if is_code_block:
            continue
        if code_block_html is not None:
            html_file.write(code_block_html)
            continue
       
        

        html_line = build_html_line(stripped_line, post, lang, is_title_image)
        html_file.write(html_line)
        
        is_title_image = False  # reset after one use
    html_file.flush()
    flush_pending_blocks(html_file,
                         table_lines, is_parsing_table,
                         unordered_list_lines, is_unordered_list,
                         code_lines, is_code_block, code_language)



def process_markdown_file(md_file_path, html_file_path, post, lang, template_manager, other_posts_section):
    """Convert a markdown file to HTML using the template manager."""
    with open(md_file_path, 'r', encoding='utf-8') as md_file, open(html_file_path, 'w', encoding='utf-8') as html_file:
        template_manager.write_header(html_file)
        html_file.write("\n<div class=\"vertical-body-container\">\n")
        parse_markdown_lines(md_file, html_file, post, lang)
        html_file.write("</div>\n</main>\n")
        html_file.write(other_posts_section)
        template_manager.write_footer(html_file)


def txt_to_html(raw_dir, posts_dir, templates_dir, posts, lang):
    prepare_output_directory(posts_dir)
    
    template_manager = TemplateManager(language=lang)
    post_processor = PostProcessor(language=lang)
    post_neighborhoods = post_processor.process_posts(posts)

    for post_neighborhood in post_neighborhoods:
        post = post_neighborhood['post']
        filename = post['file_name']
        if not filename.endswith(".md"):  
            continue
        md_file_path = os.path.join(raw_dir, filename)

        # Change the file extension from .md to .html
        html_filename = os.path.splitext(os.path.basename(filename))[0] + ".html"
        html_file_path = os.path.join(posts_dir, html_filename)
       

        if os.path.exists(html_file_path):
            print(f"{html_filename} already exists. Skipping...")
            continue

        print(f"Processing {filename} → {html_file_path}")
        process_markdown_file(md_file_path, html_file_path, post, lang, template_manager, post_neighborhood['other_posts_section'])


def markdowns_to_posts():
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
    markdowns_to_posts()