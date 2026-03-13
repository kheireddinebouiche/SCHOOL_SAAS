content = open('institut_app/views.py', 'r', encoding='utf-8').read()
content = content.replace("'approved_extensions': approved_extensions,", "'approved_extensions': all_extensions,")
open('institut_app/views.py', 'w', encoding='utf-8').write(content)
print('Fixed.')
