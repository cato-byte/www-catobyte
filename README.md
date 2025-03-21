📝 Blog Website Project - README
Welcome to the Blog Website Project! The purpose of this project is to automate the creation of HTML pages for a blog site. Each new post is processed and converted from Markdown to HTML, complete with updated metadata, navigation, and image requirements. This setup ensures the blog is consistently up-to-date and organized with every new post.

📂 Project Structure & Files
Here's a breakdown of each key component and its role in the project:

1. metadata.py 📑
Purpose: Generates essential metadata for each post, including publication dates, authorship, and navigation links.
How to Use: Run the create_metadata.py script to update or refresh metadata. This should always be executed first when adding new posts, as other scripts rely on this updated information to function correctly.
2. raw_to_post.py ✍️ ➡️ 🌐
Purpose: Transforms Markdown files (located in the raw directory) into fully formatted HTML files in the post directory.
How to Use: Run this script to convert and store your latest Markdown posts as HTML files, making them accessible on the blog.
3. create_other_post_section.py 🔗
Purpose: Updates internal navigation by linking each post to related posts or other recent entries.
How to Use: Execute after metadata.py to ensure that every post links accurately to its neighbors based on updated metadata.
4. create_posts_archive.py 📚
Purpose: Compiles a complete archive of all posts, allowing for easy access to previously published content.
How to Use: Run this script regularly to keep the archive page current with the latest posts.
5. Images 📸
Directory: images
Naming Convention: All main (title) images should follow this format: [post_name]_title_image.webp and should be 1024 x 1024 pixels for a uniform layout.
Important Note: Ensure each post has a title image. In cases where no image is available, a default image is generated.
6. create_default_img.py 🖼️
Purpose: Generates a default title image for any post lacking one, maintaining consistency across the site.
How to Use: Run this script as a last resort if certain posts are missing title images.
7. templates_to_pages.py 🖥️
Purpose: Uses predefined templates to generate static pages (like About, Contact) that are not part of the post structure.
How to Use: Run this script whenever static pages need to be generated or updated.
🚀 Execution Order
To ensure everything updates correctly, run these scripts in the following order:

Step 1: create_metadata.py 📝 – Establishes metadata for each post.
Step 2: raw_to_post.py 📄 ➡️ 🌐 – Converts Markdown to HTML and stores in the post directory.
Step 3: create_other_post_section.py 🔗 – Updates links between posts based on metadata.
Step 4: create_posts_archive.py 📚 – Updates the archive of all published posts.
Step 5: create_default_img.py 🖼️ (Optional) – Checks for and generates default images if needed.
Step 6: templates_to_pages.py 🖥️ – Creates static pages using templates.





