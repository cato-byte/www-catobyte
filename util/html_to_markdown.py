from bs4 import BeautifulSoup
import os
from pathlib import Path
from config import WEB_DIR,RAW_DIR

def html_to_markdown(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    markdown = ""
    
    # Loop through all elements in the order they appear in the HTML
    for element in soup.recursiveChildGenerator():
        if element.name == 'h2':
            markdown += f"## {element.get_text().strip()}\n\n"
        elif element.name == 'h5':
            markdown += f"**{element.get_text().strip()}**\n\n"
        elif element.name == 'img':
            alt_text = element.get('alt', '')
            src = element.get('src', '')
            markdown += f"![{alt_text}]({src})\n\n"
        elif element.name == 'h6':
            markdown += f"*{element.get_text().strip()}*\n\n"
        elif element.name == 'p':
            em = element.find('em')
            if em:
                markdown += f"*{em.get_text().strip()}*\n\n"
            else:
                markdown += f"{element.get_text().strip()}\n\n"
    
    return markdown.strip()

if __name__ == '__main__':
    # Read HTML content from a file called 'dalle3.html'
    WEB_DIR = Path(__file__).resolve().parent.parent 
    RAW_DIR = os.path.join(WEB_DIR,'raw')
    input_html = os.path.join(WEB_DIR,'post_chat_gpt_store.html')
    output_markdown = os.path.join(RAW_DIR,'chat_gpt_store.markdown')
    with open(input_html, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Convert the HTML to Markdown
    markdown_content = html_to_markdown(html_content)
    
    # Write the Markdown output to a file called 'dalle.markdown'
    with open(output_markdown , 'w', encoding='utf-8') as file:
        file.write(markdown_content)
    
    print(f"Markdown content successfully written to '{output_markdown}'")
