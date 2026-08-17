import jwt
from django.conf import settings
from channels.db import database_sync_to_async


@database_sync_to_async
def get_user(token):
    print(f"🔍 DEBUG: Token reçu = {token[:30]}...")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        print(f"🔍 DEBUG: Payload = {payload}")
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(id=payload["user_id"])
        print(f"🔍 DEBUG: User trouvé = {user.email}")
        return user
    except Exception as e:
        print(f"🔍 DEBUG: ERREUR = {e}")
        return None


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        print(f"🔍 DEBUG: Query string = {query_string[:60]}")
        
        token = None
        for param in query_string.split("&"):
            if param.startswith("token="):
                token = param.split("=", 1)[1]
                break
        
        print(f"🔍 DEBUG: Token extrait = {token is not None}")
        scope["user"] = await get_user(token) if token else None
        print(f"🔍 DEBUG: User dans scope = {scope['user']}")
        
        return await self.inner(scope, receive, send)