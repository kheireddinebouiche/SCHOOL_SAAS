from .utils import user_can

def module_access(request):
    return {
        'user_can': lambda module, permission=None, roles=None:
            user_can(
                request.user,
                module,
                permission,
                roles,
            )
    }