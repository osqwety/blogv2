import os
import re
import shutil

# Paths (using raw strings to handle Windows backslashes correctly)
posts_dir = r"C:\Users\lambo\Documents\osqwety_BLOG\content\posts"
attachments_dir = r"C:\Users\lambo\Documents\Obsidian_Vault"
static_images_dir = r"C:\Users\lambo\Documents\osqwety_BLOG\static\images"

# Step 1: Process each markdown file in the posts directory
def convert_image_links(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Initialize a flag to track if any changes were made
    content_modified = False
    
    # Regular expression to match Obsidian image links with relative paths
    image_patterns = [
        r'!\[\[([^]]+)\]\]',  # Basic Obsidian image link
        r'!\[\[\.\.\/images\/([^]]+)\]\]'  # Relative path image link
    ]
    
    # Process each image pattern
    for pattern in image_patterns:
        matches = re.findall(pattern, content)
        
        for image in matches:
            # Normalize image path (remove any leading ../ or ./)
            normalized_image = image.replace('../', '').replace('./', '')
            
            # Prepare the Markdown-compatible link
            markdown_image = f"![Image Description](/images/{normalized_image.replace(' ', '%20')}"
            
            # Find the full source path of the image
            possible_sources = [
                os.path.join(attachments_dir, normalized_image),
                os.path.join(attachments_dir, 'images', normalized_image),
                os.path.join(posts_dir, '..', 'images', normalized_image)
            ]
            
            # Find the first existing image source
            image_source = next((src for src in possible_sources if os.path.exists(src)), None)
            
            if image_source:
                # Copy the image to the Hugo static/images directory
                try:
                    shutil.copy(image_source, static_images_dir)
                    
                    # Replace the original link with the new Markdown link
                    content = content.replace(f"![[{image}]]", markdown_image)
                    content_modified = True
                    print(f"Processed image: {image}")
                except Exception as e:
                    print(f"Error processing {image}: {e}")
            else:
                print(f"Image not found: {image}")
    
    # Write back the modified content only if changes were made
    if content_modified:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
    
    return content_modified

# Process all markdown files
processed_files = 0
modified_files = 0
    
    # Walk through all markdown files in the posts directory
for root, _, files in os.walk(posts_dir):
    for filename in files:
        if filename.endswith(".md"):
            filepath = os.path.join(root, filename)
                
                # Convert image links
            if convert_image_links(filepath):
                modified_files += 1
            processed_files += 1
    
print(f"\nProcessing complete:")
print(f"Total files processed: {processed_files}")
print(f"Files modified: {modified_files}")

