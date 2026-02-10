
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.db import connection
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from importlib import import_module
from django_tenants.utils import get_tenant_model
from django.contrib.auth import get_user_model

@database_sync_to_async
def get_user(scope):
    if "headers" not in scope:
        return AnonymousUser()
        
    headers = dict(scope['headers'])
    
    # 1. Determine Tenant from Host
    try:
        host = headers.get(b'host', b'').decode().split(':')[0]
        from django_tenants.utils import get_tenant_domain_model
        domain_model = get_tenant_domain_model()
        
        try:
            domain = domain_model.objects.select_related('tenant').get(domain=host)
            tenant = domain.tenant
        except domain_model.DoesNotExist:
            print(f"Domain not found for host: {host}")
            return AnonymousUser()
            
        # Set tenant on connection for this thread
        connection.set_tenant(tenant)
        
    except Exception as e:
        print(f"Tenant resolution error: {e}")
        return AnonymousUser()
        
    # 2. Get Session and User
    try:
        cookie_header = headers.get(b'cookie', b'').decode()
        session_key = None
        for cookie in cookie_header.split('; '):
            if cookie.startswith('sessionid='):
                session_key = cookie.split('=')[1]
                break
                
        if not session_key:
            return AnonymousUser()
            
        engine = import_module(settings.SESSION_ENGINE)
        SessionStore = engine.SessionStore
        session = SessionStore(session_key)
        
        if not session.exists(session_key):
             return AnonymousUser()

        user_id = session.get('_auth_user_id')
        if user_id:
            User = get_user_model()
            try:
                user = User.objects.get(id=user_id)
                return user
            except User.DoesNotExist:
                return AnonymousUser()
                
    except Exception as e:
        print(f"User resolution error: {e}")
        
    return AnonymousUser()

class TenantAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        scope['user'] = await get_user(scope)
        return await super().__call__(scope, receive, send)
