from .utils import user_can
from ..models import GlobalConfiguration

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

def global_settings(request):
    # GlobalConfiguration is in TENANT_APPS, so its table doesn't exist in the 'public' schema.
    # We check request.tenant to avoid ProgrammingError on the public index.
    if hasattr(request, 'tenant') and request.tenant.schema_name != 'public':
        try:
            return {
                'global_config': GlobalConfiguration.get_solo()
            }
        except Exception:
            # Fallback if migrations haven't Been run for this tenant yet
            return {'global_config': None}
    return {
        'global_config': None
    }