import re

file_path = 'c:/Users/kheir/Documents/saldae/SCHOOL_SAAS/t_conseil/views.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to find the second occurrence.
# Let's split by "def ApiCreateThematique(request):"
parts = content.split('def ApiCreateThematique(request):')
if len(parts) == 3:
    # There are exactly 2 occurrences.
    # The first occurrence is correct. The second occurrence is wrong.
    # Let's rebuild the content by removing the second occurrence.
    # The second occurrence has decorators above it:
    # @login_required(login_url="institut_app:login")
    # @module_permission(allowed_modules=['conseil'])
    # def ApiCreateThematique(request):
    #   ...
    # return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    # Let's use regex to remove the second block.
    # Find the second one starting with @login_required down to status=405)
    block_regex = r'@login_required\(login_url="institut_app:login"\)\s*@module_permission\(allowed_modules=\[\'conseil\'\]\)\s*def ApiCreateThematique\(request\):[\s\S]*?return JsonResponse\(\{\'status\': \'error\', \'message\': \'Method not allowed\'\}, status=405\)'
    
    new_content = re.sub(block_regex, '', content, count=1)
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Removed second occurrence")
    else:
        print("Regex didn't match")
else:
    print(f"Found {len(parts)-1} occurrences")
