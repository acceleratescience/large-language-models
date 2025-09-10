# main.py
import os
import re # Import the regular expression module

def define_env(env):
  "Hook function"

  def list_images_in_dir(full_path, directory):
    """Helper function to list images with natural sorting."""
    
    def natural_sort_key(filename):
      """
      A key for sorting strings in a 'natural' order.
      e.g., 'Slide2.jpg' comes before 'Slide10.jpg'
      """
      # Find all sequences of digits in the filename
      parts = re.split(r'(\d+)', filename)
      # Convert the digit parts to integers for proper numeric sorting
      parts[1::2] = map(int, parts[1::2])
      return parts

    image_files = []
    if os.path.exists(full_path):
      # Use the new sorting key when sorting the directory listing
      for filename in sorted(os.listdir(full_path), key=natural_sort_key):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
          relative_path = os.path.join(directory, filename).replace("\\", "/")
          image_files.append(relative_path)
    return image_files

  @env.macro
  def slideshow_for_page():
    """
    Generates a list of images for a slideshow based on the page's
    frontmatter variable 'slides_folder'.
    """
    page = env.variables.page
    folder_name = page.meta.get('slides_folder')
    
    if not folder_name:
      return []
      
    directory = f"assets/slides/{folder_name}"
    docs_dir = 'docs'
    full_path = os.path.join(docs_dir, directory)
    
    return list_images_in_dir(full_path, directory)