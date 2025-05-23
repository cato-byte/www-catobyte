import os
from pathlib import Path

# Contact information
#Your contract email for the footer and contact sections replace if needed. 
CONTACT_EMAIL='yourcontact@email'


# Replace with your WhatsApp number in international format (no + or 00)
WHATSAPP_NUMBER = '1234567890'  

# Replace with your LinkedIn profile URL
LINKEDIN_PROFILE = 'https://www.linkedin.com/in/your-profile/'  # Replace with your LinkedIn profile URL

# Base directory of the project (automatically calculated)
# WEB_DIR points to the root directory of the project.
# Modify this if your project structure is different.
WEB_DIR = Path(__file__).resolve().parent.parent

# Raw data directory (relative to WEB_DIR)
# Replace 'raw' with the name of your raw data folder if different.
RAW_DIR = os.path.join(WEB_DIR, 'raw')

# Templates directory (relative to WEB_DIR)
# Replace 'templates' with the name of your templates folder if different.
TEMPLATES_DIR = os.path.join(WEB_DIR, 'templates')

# Templates html directory (relative to WEB_DIR)
# Replace  if different.
TEMPLATES_HTML_DIR = os.path.join(TEMPLATES_DIR, 'html')

# Templates i 18n directory (relative to WEB_DIR)
# Replace  if different.
TEMPLATES_I18N_DIR = os.path.join(TEMPLATES_DIR, 'i18n')

# Pages directory (relative to WEB_DIR)
# Replace 'pages' with the name of your pages folder if different.
PAGES_DIR = os.path.join(WEB_DIR, 'pages')

# Pages directory (relative to WEB_DIR)
# Replace 'post' with the name of your post folder if different.
PAGES_DIR = os.path.join(WEB_DIR, 'post')


# Metadata directory (relative to WEB_DIR)
# Replace 'metadata' with the name of your metadata folder if different.
METADATA_DIR = os.path.join(WEB_DIR, 'metadata')

# Metadata file (relative to WEB_DIR)
# Replace 'posts_metadata.json' with the name of your metadata file if different.
METADATA_FILE = os.path.join(WEB_DIR, 'metadata', 'posts_metadata.json')

# Supported languages
# Add or remove languages as needed.
LANGUAGES = ['en', 'es', 'fr']  # Supported languages

#URL path
# Relative paths for post folder from other html pages
# Modify if needed
RELATIVE_POST_DIR = "../../post"