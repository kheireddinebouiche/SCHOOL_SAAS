import re

with open(r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\t_exam\f_views\builltins.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the HTML content block
old_style_start = """html_content_default = \"\"\"<style>
  :root {"""

new_style_start = """html_content_default = \"\"\"<style>
  @page { margin: 1cm; }
  :root {"""

content = content.replace(old_style_start, new_style_start)

# In order to force an update on the template, we just run the code.
with open(r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\t_exam\f_views\builltins.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Margins updated successfully.")
