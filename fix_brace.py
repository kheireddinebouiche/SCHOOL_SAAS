import re

file_path = 'templates/tenant_folder/conseil/clients/details_client.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the missing brace
bad_code = """
                }
            }
);
    }
"""

good_code = """
                }
            }
        });
    }
"""

content = content.replace(bad_code, good_code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed missing brace!')
